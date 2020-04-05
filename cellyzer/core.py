"""
Main classes are modeled here

"""

from . import tools
from . import visualization
from operator import itemgetter


# Classes for Records
class Record:
    pass


class CallRecord(Record):

    def __init__(self, user, other_user, direction, duration, timestamp, cell_id, cost):
        self._user = user
        self._other_user = other_user
        self._direction = direction
        self._duration = duration
        self._timestamp = timestamp
        self._cell_id = cell_id
        self._cost = cost

    def get_user(self):
        return self._user

    def get_other_user(self):
        return self._other_user

    def get_direction(self):
        return self._direction

    def get_duration(self):
        return self._direction

    def get_timestamp(self):
        return self._timestamp

    def get_cell_id(self):
        return self._cell_id

    def get_cost(self):
        return self._cost


class MessageRecord(Record):

    def __init__(self, user, other_user, direction, length, timestamp):
        self._user = user
        self._other_user = other_user
        self._direction = direction
        self._length = length
        self._timestamp = timestamp

    def get_user(self):
        return self._user

    def get_other_user(self):
        return self._other_user

    def get_direction(self):
        return self._direction

    def get_duration(self):
        return self._length

    def get_timestamp(self):
        return self._timestamp


class CellRecord(Record):
    def __init__(self, cell_id, latitude, longitude):
        self._cell_id = cell_id
        self._latitude = latitude
        self._longitude = longitude

    def get_cell_id(self):
        return self._cell_id

    def get_latitude(self):
        return self._latitude

    def get_longitude(self):
        return self._longitude


# classes for DataSet
class DataSet:
    def __init__(self, records=None, fieldnames=None):
        self.fieldnames = fieldnames
        if records is None:
            self._records = []
        else:
            self._records = records

    def get_records(self):
        return self._records

    def add_records(self, data):
        self._records.append(data)

    def get_max(self):
        return self._records

    def get_columns(self):
        print("columns")

    def get_rows(self):
        print("rows")


class CallDataSet(DataSet):
    def get_all_users(self):
        # return all the different users in the CallDataSet
        all_users = []
        for record in super().get_records():
            user = record.get_user()
            other_user = record.get_other_user()
            if user not in all_users:
                all_users.append(user)
            if other_user not in all_users:
                all_users.append(other_user)
        return all_users

    def get_records(self, user1=None, user2=None):
        # filter records using given user(s)
        connection_reords = []
        for record in super().get_records():
            user = record.get_user()
            other_user = record.get_other_user()
            if (user1 is None) and (user2 is None):
                # calls the function of Dataset class
                return super().get_records()
            if (user1 is not None) and (user2 is None):
                # returns a list of CallRecord objects where the given user is involved
                if user1 == user or user1 == other_user:
                    connection_reords.append(record)
            if (user1 is not None) and (user2 is not None):
                # returns a list of CallRecord objects where the gicen 2 users are involved
                if (user1 == user and user2 == other_user) or (user1 == other_user and user2 == user):
                    connection_reords.append(record)
        return connection_reords

    def get_connected_users(self, user):
        # returns the list of users that are connected to the given user
        connected_users = []
        for record in self.get_records(user):
            user1 = record.get_user()
            user2 = record.get_other_user()
            if (user1 not in connected_users) and (user1 != user):
                connected_users.append(user1)
            if (user2 not in connected_users) and (user2 != user):
                connected_users.append(user2)
        return connected_users

    def print_connection_matrix(self):
        matrix = []
        all_users = self.get_all_users()
        for u1 in all_users:
            connected_users = self.get_connected_users(u1)
            row = []
            for u2 in all_users:
                if u2 in connected_users:
                    weight = len(self.get_records(u1, u2))
                    row.append(weight)
                else:
                    row.append(".")
            matrix.append(row)
        tools.print_matrix(matrix, all_users)

    def get_connections(self):
        connections = []
        for record in self.get_records():
            connection = [record.get_user(), record.get_other_user()]
            connections.append(connection)
        return connections

    def visualize_connection_network(self, directed=True):
        connections = self.get_connections()
        visualization.network_graph(connections, directed)

    def get_close_contacts(self, user, top_contact=5):
        connected_users = self.get_connected_users(user)
        contacts_dict = {}
        for user2 in connected_users:
            records = self.get_records(user, user2)
            contacts_dict[user2] = len(records)
        close_contacts = dict(sorted(contacts_dict.items(), key=itemgetter(1), reverse=True)[:top_contact])
        return close_contacts

    def get_most_active_time(self):
        print("most active time")

    def get_call_details(self):
        print("call details")


class MessageDataSet(DataSet):

    def get_all_users(self):
        # return all the different users in the MessageDataSet
        all_users = []
        for record in super().get_records():
            user = record.get_user()
            other_user = record.get_other_user()
            if user not in all_users:
                all_users.append(user)
            if other_user not in all_users:
                all_users.append(other_user)

        return all_users

    def get_records(self, user1=None, user2=None):
        # filter records using given user(s)
        connection_records = []
        for record in super().get_records():
            user = record.get_user()
            other_user = record.get_other_user()
            if (user1 is None) and (user2 is None):
                # calls the function of DataSet class
                return super().get_records()
            if (user1 is not None) and (user2 is None):
                # returns a list of MessageRecord objects where the given user is involved
                if user1 == user or user1 == other_user:
                    connection_records.append(record)
            if (user1 is not None) and (user2 is not None):
                # returns a list of MessageRecord objects where the given 2 users are involved(connected)
                if (user1 == user and user2 == other_user) or (user1 == other_user and user2 == user):
                    connection_records.append(record)
        return connection_records

    def get_connected_users(self, user):
        # returns the list of users that are connected to the given user
        connected_users = []
        for record in self.get_records(user):
            user1 = record.get_user()
            user2 = record.get_other_user()
            if (user1 not in connected_users) and (user1 != user):
                connected_users.append(user1)
            if (user2 not in connected_users) and (user2 != user):
                connected_users.append(user2)
        return connected_users

    def print_connection_matrix(self):

        matrix = []
        all_users = self.get_all_users()
        for u1 in all_users:
            connected_users = self.get_connected_users(u1)
            row = []
            for u2 in all_users:
                if u2 in connected_users:

                    weight = len(self.get_records(u1, u2))
                    row.append(weight)
                else:
                    row.append(".")
            matrix.append(row)
        tools.print_matrix(matrix, all_users)

    def get_connections(self):
        connections = []
        for record in self.get_records():
            connection = [record.get_user(), record.get_other_user()]
            connections.append(connection)
        return connections

    def visualize_connection_network(self, directed=True):
        connections = self.get_connections()
        visualization.network_graph(connections, directed)

    def get_close_contacts(self):
        print("close contacts")

    def get_frequenct_conversations(self):
        print("Frequent conversations between ")


class CellDataSet(DataSet):
    def get_population(self, cell_id):
        print("close contacts around = ", cell_id)


# class User
class User:
    def __init__(self, contact_no):
        self._contact_no = contact_no

    def get_contact_no(self):
        return self._contact_no

    def get_trip(self):
        print("trips")

    def get_home_location(self):
        print("home location = xxx . xxx")

    def get_work_location(self):
        print("work location = xxx . xxx")

    def get_ignored_calls(self):
        print("ignored calls = 111222333")
