import sqlite3
import csv

def execute_and_export_sql_queries(database_path, output_paths, sql_statements):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Create a list to store result sets
    results = []

    # Execute SQL statements
    for statement in sql_statements:
        cursor.execute(statement)
        results.append(cursor.fetchall())

    # Write results to CSV files
    for idx, output_path in enumerate(output_paths):
        cursor.execute(sql_statements[idx])  # Re-execute the query to get column descriptions
        csv_headers = [column[0] for column in cursor.description]

        with open(output_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(csv_headers)
            csvwriter.writerows(results[idx])

    # Close the cursor and connection
    cursor.close()
    conn.close()

# Example usage:
database_path = '/home/cristel/Desktop/Internship/zotero.sqlite'
output_paths = [
    '/home/cristel/Desktop/Stage/collections_data.csv',
    '/home/cristel/Desktop/Stage/items_data.csv',
    '/home/cristel/Desktop/Stage/itemtypes_data.csv',
    '/home/cristel/Desktop/Stage/collectionitems_data.csv'
]
sql_statements = [
    "SELECT collectionID, collectionName, collections.key AS collectionKey FROM collections;",
    "SELECT itemID, itemTypeID, items.key AS itemKey FROM items;",
    "SELECT itemTypeID, typeName FROM itemTypes;",
    "SELECT collectionID, itemID FROM collectionItems;"  # Add the query for collectionItems
]

execute_and_export_sql_queries(database_path, output_paths, sql_statements)
