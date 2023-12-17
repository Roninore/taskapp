from enum import StrEnum

from pydantic import BaseModel

from taskapp.repository.task import Task, TaskState
from taskapp.repository.user import UserRole, UserWithoutSecrets


class UserProfileStatusEnum(StrEnum):
    ok = "ok"
    user_not_found = "user_not_found"


class UserProfileResponse(BaseModel):
    status: UserProfileStatusEnum
    username: str | None = None
    role: UserRole | None = None
    username: str | None = None
    full_name: str | None = None


class GetMyTasksStatus(StrEnum):
    ok = "ok"


class GetMyTasksResponse(BaseModel):
    status: GetMyTasksStatus
    tasks: list[Task]


class GetTasksStatus(StrEnum):
    ok = "ok"


class GetTasksResponse(BaseModel):
    status: GetTasksStatus
    tasks: list[Task]


class UpdateUserStatus(StrEnum):
    ok = "ok"


class UpdateUserResponse(BaseModel):
    status: UpdateUserStatus


class UpdateUserBody(BaseModel):
    user_id: int
    username: str
    full_name: str
    role: UserRole


class GetUseresStatus(StrEnum):
    ok = "ok"


class GetUserResponse(BaseModel):
    status: GetUseresStatus
    users: list[UserWithoutSecrets]


class CreateUserStatus(StrEnum):
    ok = "ok"


class CreateUserResponse(BaseModel):
    status: CreateUserStatus


class CreateUserBody(BaseModel):
    username: str
    full_name: str
    role: UserRole
    password: str


class ChangePasswordStatus(StrEnum):
    ok = "ok"


class ChangePasswordResponse(BaseModel):
    status: ChangePasswordStatus


class ChangePasswordBody(BaseModel):
    user_id: int
    password: str


class DeleteUserStatus(StrEnum):
    ok = "ok"


class DeleteUserResponse(BaseModel):
    status: DeleteUserStatus


class DeleteUserBody(BaseModel):
    user_id: int


class AddPerformerStatus(StrEnum):
    ok = "ok"


class AddPerformerResponse(BaseModel):
    status: AddPerformerStatus


class AddPerformerBody(BaseModel):
    user_id: int
    task_id: int


class DeletePerformerStatus(StrEnum):
    ok = "ok"


class DeletePerformerResponse(BaseModel):
    status: DeletePerformerStatus


class DeletePerformerBody(BaseModel):
    user_id: int
    task_id: int


class UpdateTaskStatus(StrEnum):
    ok = "ok"


class UpdateTaskResponse(BaseModel):
    status: UpdateTaskStatus


class UpdateTaskBody(BaseModel):
    task_id: int
    caption: str
    text: str
    state: TaskState


class CreateTaskStatus(StrEnum):
    ok = "ok"


class CreateTaskResponse(BaseModel):
    status: UpdateTaskStatus


class CreateTaskBody(BaseModel):
    caption: str
    text: str
    state: TaskState
    performers: list[int]


class UpdateTaskStateBody(BaseModel):
    task_id: int
    new_state: TaskState


class UpdateTaskStateStatus(StrEnum):
    ok = "ok"
    not_enough_rights = "not_enough_rights"


class UpdateTaskStateResponse(BaseModel):
    status: UpdateTaskStateStatus
