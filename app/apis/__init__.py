from flask_restx import Api

api = Api(
    title="Learning SQLAlchemy",
    version="2.0",
    doc="/api/docs",
)

# api.add_namespace(ns, path="/api/ns")