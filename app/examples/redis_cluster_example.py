#!/usr/bin/env python
"""
Example usage of the Redis Cluster client.
This script demonstrates how to use the RedisClusterClient for distributed Redis operations.
"""

import os
import sys
import json
import time
from dotenv import load_dotenv

# Add the parent directory to the path so we can import the app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.redis_cluster_client import RedisClusterClient

# Load environment variables
load_dotenv()

def main():
    """Main function demonstrating Redis Cluster client usage."""
    print("Redis Cluster Client Example")
    print("===========================")
    
    # Initialize the Redis Cluster client
    # You can specify multiple nodes for redundancy
    startup_nodes = [
        {"host": os.getenv('REDIS_CLUSTER_HOST', 'localhost'), 
         "port": int(os.getenv('REDIS_CLUSTER_PORT', 6379))}
    ]
    
    # Add more nodes if you have a multi-node cluster
    # startup_nodes.append({"host": "redis2.example.com", "port": 6379})
    # startup_nodes.append({"host": "redis3.example.com", "port": 6379})
    
    client = RedisClusterClient(
        startup_nodes=startup_nodes,
        password=os.getenv('REDIS_CLUSTER_PASSWORD', None)
    )
    
    try:
        # Basic key-value operations
        print("\n1. Basic Key-Value Operations")
        print("-----------------------------")
        
        # Set a string value
        client.set("example:string", "Hello, Redis Cluster!")
        print("Set string value: 'example:string' = 'Hello, Redis Cluster!'")
        
        # Get the string value
        value = client.get("example:string")
        print(f"Got string value: {value}")
        
        # Set a JSON value
        user_data = {
            "id": 123,
            "name": "John Doe",
            "email": "john@example.com",
            "preferences": {
                "theme": "dark",
                "notifications": True
            }
        }
        client.set("example:user:123", user_data)
        print(f"Set JSON value: 'example:user:123' = {json.dumps(user_data, indent=2)}")
        
        # Get the JSON value
        user = client.get("example:user:123")
        print(f"Got JSON value: {json.dumps(user, indent=2)}")
        
        # Set with expiration
        client.set("example:temp", "This will expire in 5 seconds", expire=5)
        print("Set temporary value with 5-second expiration")
        
        # Check if the key exists
        exists = client.exists("example:temp")
        print(f"Key exists: {exists}")
        
        # Wait for expiration
        print("Waiting 6 seconds for expiration...")
        time.sleep(6)
        
        # Check if the key still exists
        exists = client.exists("example:temp")
        print(f"Key exists after expiration: {exists}")
        
        # Hash operations
        print("\n2. Hash Operations")
        print("-----------------")
        
        # Set hash fields
        product_data = {
            "id": "P123",
            "name": "Smartphone",
            "price": "999.99",
            "stock": "50",
            "category": "electronics"
        }
        client.set_hash("example:product:123", product_data)
        print(f"Set hash: 'example:product:123' = {json.dumps(product_data, indent=2)}")
        
        # Get all hash fields
        product = client.get_hash("example:product:123")
        print(f"Got hash: {json.dumps(product, indent=2)}")
        
        # Get a specific hash field
        price = client.get_hash_field("example:product:123", "price")
        print(f"Got hash field 'price': {price}")
        
        # Update a hash field
        client.set_hash("example:product:123", {"stock": "45"})
        print("Updated hash field 'stock' to '45'")
        
        # Get the updated hash
        product = client.get_hash("example:product:123")
        print(f"Got updated hash: {json.dumps(product, indent=2)}")
        
        # List operations
        print("\n3. List Operations")
        print("-----------------")
        
        # Push values to a list
        recent_users = ["user:1", "user:2", "user:3", "user:4", "user:5"]
        client.push_list("example:recent_users", *recent_users)
        print(f"Pushed to list: {recent_users}")
        
        # Get list values
        users = client.get_list("example:recent_users")
        print(f"Got list: {users}")
        
        # Get a subset of the list
        recent = client.get_list("example:recent_users", 0, 2)
        print(f"Got recent users: {recent}")
        
        # Set operations
        print("\n4. Set Operations")
        print("----------------")
        
        # Add values to a set
        categories = ["electronics", "clothing", "books", "food"]
        client.add_to_set("example:categories", *categories)
        print(f"Added to set: {categories}")
        
        # Get set values
        cats = client.get_set("example:categories")
        print(f"Got set: {cats}")
        
        # Cluster-specific operations
        print("\n5. Cluster Operations")
        print("--------------------")
        
        # Get cluster nodes
        nodes = client.get_cluster_nodes()
        print(f"Cluster nodes: {json.dumps(nodes, indent=2)}")
        
        # Get cluster slots
        slots = client.get_cluster_slots()
        print(f"Cluster slots: {json.dumps(slots, indent=2)}")
        
        # Get key slot
        key = "example:string"
        slot = client.get_key_slot(key)
        print(f"Slot for key '{key}': {slot}")
        
        # Get node for key
        node = client.get_node_for_key(key)
        print(f"Node for key '{key}': {json.dumps(node, indent=2)}")
        
        # Pub/Sub operations
        print("\n6. Pub/Sub Operations")
        print("--------------------")
        
        # Publish a message
        message = {"event": "user_login", "user_id": 123, "timestamp": time.time()}
        result = client.publish("example:events", message)
        print(f"Published message: {json.dumps(message, indent=2)}")
        print(f"Message received by {result} subscribers")
        
        print("\nExample completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the client
        client.close()
        print("Redis Cluster client closed")

if __name__ == "__main__":
    main() 