import asyncio

import grpc
from grpc import aio

from .. import crud
from ..db.session import SessionLocal
from ..grpc import glossary_pb2, glossary_pb2_grpc


class GlossaryServicer(glossary_pb2_grpc.GlossaryServiceServicer):
    async def ListTerms(self, request, context):
        db = SessionLocal()
        try:
            names = crud.list_term_names(db)
            return glossary_pb2.TermNames(names=names)
        finally:
            db.close()

    async def GetTerm(self, request, context):
        db = SessionLocal()
        try:
            t = crud.get_term_by_name(db, request.name)
            if not t:
                return glossary_pb2.TermResponse(found=False, error="Not found")
            return glossary_pb2.TermResponse(
                name=t.name, description=t.description, found=True
            )
        finally:
            db.close()

    async def CreateTerm(self, request, context):
        db = SessionLocal()
        try:
            from ..schemas import TermCreate

            try:
                obj = crud.create_term(
                    db, TermCreate(name=request.name, description=request.description)
                )
                return glossary_pb2.TermResponse(
                    name=obj.name, description=obj.description, found=True
                )
            except Exception as e:
                return glossary_pb2.TermResponse(found=False, error=str(e))
        finally:
            db.close()

    async def UpdateTerm(self, request, context):
        db = SessionLocal()
        try:
            obj = crud.update_term(
                db,
                request.current_name,
                request.new_name or None,
                request.new_description or None,
            )
            if not obj:
                return glossary_pb2.TermResponse(found=False, error="Not found")
            return glossary_pb2.TermResponse(
                name=obj.name, description=obj.description, found=True
            )
        finally:
            db.close()

    async def DeleteTerm(self, request, context):
        db = SessionLocal()
        try:
            ok = crud.delete_term(db, request.name)
            return glossary_pb2.DeleteResponse(ok=ok, error="" if ok else "Not found")
        finally:
            db.close()


async def serve(host="0.0.0.0", port=50051):
    server = aio.server()
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryServicer(), server)
    server.add_insecure_port(f"{host}:{port}")
    await server.start()
    print(f"gRPC server started on {host}:{port}")
    await server.wait_for_termination()
