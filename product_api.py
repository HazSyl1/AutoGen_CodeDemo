Here’s a basic structure for a Flask-based Product Catalog API that meets typical expectations from such a Jira Story.

```python
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# In-memory product catalog (simulate DB)
products = {}
product_id_seq = 1

# ---- Models ----
def product_repr(prod):
    """Format product for API response."""
    return {
        "id": prod["id"],
        "name": prod["name"],
        "description": prod.get("description", ""),
        "price": prod.get("price", 0.0),
        "category": prod.get("category", "")
    }

# ---- Routes ----

# List products
@app.route('/products', methods=['GET'])
def list_products():
    return jsonify([product_repr(p) for p in products.values()]), 200

# Create a new product
@app.route('/products', methods=['POST'])
def add_product():
    global product_id_seq
    data = request.get_json()
    required = ['name', 'price']
    if not all(k in data for k in required):
        abort(400, "Missing name or price in request body.")

    prod = {
        "id": product_id_seq,
        "name": data['name'],
        "description": data.get("description", ""),
        "price": float(data['price']),
        "category": data.get("category", "")
    }
    products[product_id_seq] = prod
    product_id_seq += 1
    return jsonify(product_repr(prod)), 201

# Get product by ID
@app.route('/products/<int:pid>', methods=['GET'])
def get_product(pid):
    prod = products.get(pid)
    if not prod:
        abort(404, "Product not found.")
    return jsonify(product_repr(prod)), 200

# Update product
@app.route('/products/<int:pid>', methods=['PUT'])
def update_product(pid):
    prod = products.get(pid)
    if not prod:
        abort(404, "Product not found.")
    data = request.get_json()
    if "name" in data:
        prod["name"] = data["name"]
    if "description" in data:
        prod["description"] = data["description"]
    if "price" in data:
        prod["price"] = float(data["price"])
    if "category" in data:
        prod["category"] = data["category"]
    return jsonify(product_repr(prod)), 200

# Delete product
@app.route('/products/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    if pid not in products:
        abort(404, "Product not found.")
    del products[pid]
    return '', 204

# ---- Run server ----
if __name__ == "__main__":
    app.run(debug=True)
```

**Features:**
- CRUD operations for products.
- Uses JSON for request/response.
- Simple in-memory storage simulating a database.

**Note:** For production, you’d use a real database and add authentication, validation, error handling, and pagination. Let me know if you need those!