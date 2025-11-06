"""
Data processing module
"""

import json
from typing import Any, Dict, List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..utils.logger import get_logger


class DataProcessor:
    """Data processor for handling various data operations"""

    def __init__(self, max_workers: int = 4):
        """Initialize data processor

        Args:
            max_workers: Maximum number of worker threads
        """
        self.max_workers = max_workers
        self.logger = get_logger()

    def process_batch(self, items: List[Any], process_func: Callable) -> List[Any]:
        """Process batch of items in parallel

        Args:
            items: List of items to process
            process_func: Function to apply to each item

        Returns:
            List of processed results
        """
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_item = {executor.submit(process_func, item): item for item in items}

            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Error processing item {item}: {e}")
                    results.append(None)

        return results

    def filter_data(self, data: List[Dict], conditions: Dict[str, Any]) -> List[Dict]:
        """Filter data based on conditions

        Args:
            data: List of dictionaries to filter
            conditions: Dictionary of field: value conditions

        Returns:
            Filtered list of dictionaries
        """
        filtered = []
        for item in data:
            match = True
            for key, value in conditions.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                filtered.append(item)
        return filtered

    def transform_data(self, data: List[Dict], transformations: Dict[str, Callable]) -> List[Dict]:
        """Transform data using provided transformation functions

        Args:
            data: List of dictionaries to transform
            transformations: Dictionary of field: transformation_function

        Returns:
            Transformed list of dictionaries
        """
        transformed = []
        for item in data.copy():
            new_item = item.copy()
            for field, transform_func in transformations.items():
                if field in new_item:
                    try:
                        new_item[field] = transform_func(new_item[field])
                    except Exception as e:
                        self.logger.error(f"Error transforming field {field}: {e}")
            transformed.append(new_item)
        return transformed

    def aggregate_data(self, data: List[Dict], group_by: str, aggregations: Dict[str, str]) -> Dict:
        """Aggregate data by grouping and applying aggregation functions

        Args:
            data: List of dictionaries to aggregate
            group_by: Field to group by
            aggregations: Dictionary of field: aggregation_type (sum, avg, count, min, max)

        Returns:
            Dictionary of aggregated results
        """
        groups = {}

        # Group data
        for item in data:
            if group_by not in item:
                continue
            group_key = item[group_by]
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(item)

        # Aggregate each group
        results = {}
        for group_key, group_items in groups.items():
            results[group_key] = {}
            for field, agg_type in aggregations.items():
                values = [item.get(field, 0) for item in group_items if field in item]

                if agg_type == "sum":
                    results[group_key][f"{field}_{agg_type}"] = sum(values)
                elif agg_type == "avg":
                    results[group_key][f"{field}_{agg_type}"] = sum(values) / len(values) if values else 0
                elif agg_type == "count":
                    results[group_key][f"{field}_{agg_type}"] = len(values)
                elif agg_type == "min":
                    results[group_key][f"{field}_{agg_type}"] = min(values) if values else None
                elif agg_type == "max":
                    results[group_key][f"{field}_{agg_type}"] = max(values) if values else None

        return results

    def export_to_json(self, data: Any, filepath: str) -> None:
        """Export data to JSON file

        Args:
            data: Data to export
            filepath: Path to output file
        """
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        self.logger.info(f"Data exported to {filepath}")

    def import_from_json(self, filepath: str) -> Any:
        """Import data from JSON file

        Args:
            filepath: Path to input file

        Returns:
            Imported data
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        self.logger.info(f"Data imported from {filepath}")
        return data
