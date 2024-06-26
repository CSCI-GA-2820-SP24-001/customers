######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Customer Store Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Customers from the inventory of customers in the CustomerShop
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Customer
from service.common import status  # HTTP Status Codes


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")

######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# READ A Customer
######################################################################


@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers(customer_id):
    """
    Retrieve a single customer

    This endpoint will return a customer based on it's id
    """
    app.logger.info("Request for customer with id: %s", customer_id)

    customer = Customer.find(customer_id)
    if not customer:
        error(
            status.HTTP_404_NOT_FOUND,
            f"customer with id '{customer_id}' was not found.",
        )

    app.logger.info("Returning customer: %s", customer.name)
    return jsonify(customer.serialize()), status.HTTP_200_OK


######################################################################
# CREATE A NEW CUSTOMER
######################################################################
@app.route("/customers", methods=["POST"])
def create_customers():
    """
    Creates a Customer

    This endpoint will create a Customer based the data in the body that is posted
    """
    app.logger.info("Request to create a customer")
    check_content_type("application/json")

    customer = Customer()
    customer.deserialize(request.get_json())
    customer.create()
    message = customer.serialize()
    location_url = url_for("get_customers", customer_id=customer.id, _external=True)

    app.logger.info("Customer with ID: %d created.", customer.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# UPDATE AN EXISTING Customer
######################################################################
@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customers(customer_id):
    """
    Update a Customer

    This endpoint will update a Customer based the body that is posted
    """
    app.logger.info("Request to update customer with id: %d", customer_id)
    check_content_type("application/json")

    customer = Customer.find(customer_id)
    if not customer:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Customer with id: '{customer_id}' was not found.",
        )

    customer.deserialize(request.get_json())
    customer.id = customer_id
    customer.update()

    app.logger.info("Customer with ID: %d updated.", customer.id)
    return jsonify(customer.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    """
    Delete a Customer

    This endpoint will delete a Customer based the id specified in the path
    """
    app.logger.info("Request to delete customer with id: %d", customer_id)

    customer = Customer.find(customer_id)
    if customer:
        customer.delete()

    app.logger.info("Customer with ID: %d delete complete.", customer_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# LIST ALL CUSTOMERS
######################################################################
@app.route("/customers", methods=["GET"])
def list_customers():
    """Returns all of the Customers"""
    app.logger.info("Request for customer list")

    customers = []

    # See if any query filters were passed in
    address = request.args.get("address")
    name = request.args.get("name")
    email = request.args.get("email")
    phonenumber = request.args.get("phonenumber")
    if address:
        customers = Customer.find_by_address(address)
    elif name:
        customers = Customer.find_by_name(name)
    elif email:
        customers = Customer.find_by_email(email)
    elif phonenumber:
        customers = Customer.find_by_phonenumber(phonenumber)
    else:
        customers = Customer.all()

    results = [customer.serialize() for customer in customers]
    app.logger.info("Returning %d customers", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        error(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    error(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# Logs error messages before aborting
######################################################################
def error(status_code, reason):
    """Logs the error and then aborts"""
    app.logger.error(reason)
    abort(status_code, reason)
