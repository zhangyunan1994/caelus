from flask import Flask, jsonify, render_template, request
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy
from db_util import get_databases, get_tables, get_columns, get_connection_columns


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'elf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class TBConnection(db.Model):
    __tablename__ = 'tb_database'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    host = db.Column('host', db.String)
    port = db.Column('port', db.Integer)
    user = db.Column('user', db.String)
    password = db.Column('password', db.String)
    status = db.Column('status', db.Integer, default=0)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


@app.route("/")
def index():
    return render_template('index.html')


"""
查询已经创建的所有连接
"""
@app.route("/connection")
def connections():
    connections = TBConnection.query.all()
    # 总会遇到这么尬的问题
    result = [connection.to_dict() for connection in connections]
    return jsonify(result)


"""
创建连接
"""
@app.route("/connection", methods=["POST"])
def add_connections():
    param = request.get_json()
    connection = TBConnection()
    connection.name = param.get('name')
    connection.host = param.get('host')
    connection.port = param.get('port')
    connection.user = param.get('user')
    connection.password = param.get('password')
    db.session.add(connection)
    db.session.commit()
    return jsonify({"message": "恭喜你创建成功"})


"""
删除一个已有的连接
"""
@app.route("/connection/<int:id>", methods=["DELETE"])
def del_connections(id):
    connection = TBConnection.query.filter_by(id=id).first()
    if not connection:
        return jsonify({"message": "恭喜你，删除失败，我都开始鄙视你了."})
    db.session.delete(connection)
    db.session.commit()
    return jsonify({"message": "恭喜你删除成功，再接再厉."})


@app.route("/connection/<int:id>/database")
def connection_database(id):
    connection = TBConnection.query.filter_by(id=id).first()
    if not connection:
        return jsonify({"code": "500", "message": "恭喜你，什么都没查到，我都开始鄙视你了."})
    databases = get_databases(host=connection.host, port=connection.port, user=connection.user, password=connection.password)
    return jsonify([database[0] for database in databases])


@app.route("/connection/<int:id>/database/<database>/table")
def connection_database_table(id, database):
    connection = TBConnection.query.filter_by(id=id).first()
    if not connection:
        return jsonify({"code": "500", "message": "恭喜你，什么都没查到，我都开始鄙视你了."})
    tables = get_tables(host=connection.host, port=connection.port, user=connection.user,
                           password=connection.password, database=database)
    return jsonify([{"name": table[0], "comment": table[1]} for table in tables])


@app.route("/connection/<int:id>/database/<database>/table/<table>/column")
def connection_database_table_column(id, database, table):
    connection = TBConnection.query.filter_by(id=id).first()
    if not connection:
        return jsonify({"code": "500", "message": "恭喜你，什么都没查到，我都开始鄙视你了."})
    columns = get_columns(host=connection.host, port=connection.port, user=connection.user,
                           password=connection.password, database=database, table=table)
    return jsonify([{"schema": column[0],
                     "table": column[1],
                     "column": column[2],
                     "nullable": column[3],
                     "type": column[4],
                     "comment": column[5],
                     "default": column[6],
                     } for column in columns])


@app.route("/connection/<int:id>/column/<column>")
def connection_column(id, column):
    connection = TBConnection.query.filter_by(id=id).first()
    if not connection:
        return jsonify({"code": "500", "message": "恭喜你，什么都没查到，我都开始鄙视你了."})
    columns = get_connection_columns(host=connection.host, port=connection.port, user=connection.user,
                           password=connection.password, column=column)
    return jsonify([{"schema": column[0],
                     "table": column[1],
                     "column": column[2],
                     "nullable": column[3],
                     "type": column[4],
                     "comment": column[5],
                     "default": column[6],
                     } for column in columns])


if __name__ == '__main__':
    app.run()
