from functools import wraps


from ub_backend.database.postgres.db import session


class Transactional:
    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            try:
                result = await function(*args, **kwargs)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

            return result

        return decorator
