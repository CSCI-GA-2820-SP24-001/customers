"""
Test cases for Customer Model
"""

import os
import logging
from unittest import TestCase
from unittest.mock import patch
from wsgi import app
from service.models import Customer, DataValidationError, db
from .factories import CustomerFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################

#  C U S T O M E R   M O D E L   T E S T   C A S E S


######################################################################
# pylint: disable=too-many-public-methods
class TestCustomer(TestCase):
    """Test Cases for Customer Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_customer(self):
        """It should create a Customer"""
        customer = CustomerFactory()
        customer.create()
        self.assertIsNotNone(customer.id)
        found = Customer.all()
        self.assertEqual(len(found), 1)
        data = Customer.find(customer.id)
        self.assertEqual(data.name, customer.name)
        self.assertEqual(data.address, customer.address)
        self.assertEqual(data.email, customer.email)
        self.assertEqual(data.phonenumber, customer.phonenumber)

    def test_read_a_customer(self):
        """It should Read a customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        customer.create()
        self.assertIsNotNone(customer.id)
        # Fetch it back
        found_customer = customer.find(customer.id)
        self.assertEqual(found_customer.id, customer.id)
        self.assertEqual(found_customer.name, customer.name)
        self.assertEqual(found_customer.address, customer.address)
        self.assertEqual(found_customer.email, customer.email)
        self.assertEqual(found_customer.phonenumber, customer.phonenumber)

    def test_update_a_customer(self):
        """It should Update a Customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        customer.create()
        logging.debug(customer)
        self.assertIsNotNone(customer.id)
        # Change it an save it
        customer.name = "Billy the Kid"
        original_id = customer.id
        customer.update()
        self.assertEqual(customer.id, original_id)
        self.assertEqual(customer.name, "Billy the Kid")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].id, original_id)
        self.assertEqual(customers[0].name, "Billy the Kid")

    def test_update_no_id(self):
        """It should not Update a Customer with no id"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        self.assertRaises(DataValidationError, customer.update)

    def test_delete_a_customer(self):
        """It should Delete a Customer"""
        customer = CustomerFactory()
        customer.create()
        self.assertEqual(len(Customer.all()), 1)
        # delete the customer and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(Customer.all()), 0)

    def test_serialize_a_customer(self):
        """It should serialize a Customer"""
        customer = CustomerFactory()
        data = customer.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], customer.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], customer.name)
        self.assertIn("email", data)
        self.assertEqual(data["email"], customer.email)
        self.assertIn("address", data)
        self.assertEqual(data["address"], customer.address)
        self.assertIn("phonenumber", data)
        self.assertEqual(data["phonenumber"], customer.phonenumber)

    def test_deserialize_a_customer(self):
        """It should de-serialize a customer"""
        data = CustomerFactory().serialize()
        customer = Customer()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, data["name"])
        self.assertEqual(customer.address, data["address"])
        self.assertEqual(customer.email, data["email"])
        self.assertEqual(customer.phonenumber, data["phonenumber"])

    def test_deserialize_missing_data(self):
        """It should not deserialize a Customer with missing data"""
        data = {"id": 1, "name": "Billy the Kid", "email": "BillytheKid@gmail.com"} #phonenumber and adress are missing
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_deserialize_bad_name(self):
        """It should not deserialize a bad name attribute"""
        test_customer = CustomerFactory()
        data = test_customer.serialize()
        data["name"] = 45
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_list_all_customers(self):
        """It should List all Customers in the database"""
        customers = Customer.all()
        self.assertEqual(customers, [])
        # Create 5 Customers
        for _ in range(5):
            customer = CustomerFactory()
            customer.create()
        # See if we get back 5 customers
        customers = Customer.all()
        self.assertEqual(len(customers), 5)


######################################################################
#  T E S T   E X C E P T I O N   H A N D L E R S
######################################################################
class TestExceptionHandlers(TestCustomer):
    """Customer Model Exception Handlers"""

    @patch("service.models.db.session.commit")
    def test_create_exception(self, exception_mock):
        """It should catch a create exception"""
        exception_mock.side_effect = Exception()
        customer = CustomerFactory()
        self.assertRaises(DataValidationError, customer.create)

    @patch("service.models.db.session.commit")
    def test_update_exception(self, exception_mock):
        """It should catch a update exception"""
        exception_mock.side_effect = Exception()
        customer = CustomerFactory()
        self.assertRaises(DataValidationError, customer.update)

    @patch("service.models.db.session.commit")
    def test_delete_exception(self, exception_mock):
        """It should catch a delete exception"""
        exception_mock.side_effect = Exception()
        customer = CustomerFactory()
        self.assertRaises(DataValidationError, customer.delete)


######################################################################
#  Q U E R Y   T E S T   C A S E S
######################################################################
class TestModelQueries(TestCustomer):
    """Customer Model Query Tests"""

    def test_find_customer(self):
        """It should Find a Customer by ID"""
        customers = CustomerFactory.create_batch(5)
        for customer in customers:
            customer.create()
        logging.debug(customers)
        # make sure they got saved
        self.assertEqual(len(Customer.all()), 5)
        # find the 2nd customer in the list
        customer = Customer.find(customers[1].id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.id, customers[1].id)
        self.assertEqual(customer.name, customers[1].name)
        self.assertEqual(customer.address, customers[1].address)
        self.assertEqual(customer.email, customers[1].email)
        self.assertEqual(customer.phonenumber, customers[1].phonenumber)

    def test_find_by_name(self):
        """It should Find a Customer by Name"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        name = customers[0].name
        count = len([customer for customer in customers if customer.name == name])
        found = Customer.find_by_name(name)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.name, name)

    # # ToDo deserialize tests for data types with restrictions
    # def test_deserialize_bad_address(self): if that is right, there is a rigidness to the example data types
    #    """It should not deserialize a bad address attribute"""
    #    test_customer = CustomerFactory()
    #    data = test_customer.serialize()
    #    data["address"] = "male"  # wrong case
    #    customer = Customer()
    #    self.assertRaises(DataValidationError, customer.deserialize, data)
