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
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


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
    # Todo: uncomment this code when get_accounts is implemented
    # location_url = url_for("get_customers", customer_id=customer.id, _external=True)
    location_url = "unknown"

    app.logger.info("Customer with ID: %d created.", customer.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


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


######################################################################
# DELETE A PET
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
# READ A PET
######################################################################
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers(customer_id):
    """
    Retrieve a single Customer

    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for customer with id: %s", customer_id)

    customer = Customer.find(customer_id)
    if not customer:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Customer with id '{customer_id}' was not found.",
        )

    app.logger.info("Returning customer: %s", customer.name)
    return jsonify(customer.serialize()), status.HTTP_200_OK
