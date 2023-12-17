import logging

from fastapi import APIRouter, Depends

from taskapp.repository.session import Session
from taskapp.state import app_state
from taskapp.views.auth.helpers import (
    check_admin_session,
    check_manager_session,
    check_session,
    get_password_hash,
)

from .models import (
    AddPerformerBody,
    AddPerformerResponse,
    AddPerformerStatus,
    ChangePasswordBody,
    ChangePasswordResponse,
    ChangePasswordStatus,
    CreateTaskBody,
    CreateTaskResponse,
    CreateTaskStatus,
    CreateUserBody,
    CreateUserResponse,
    CreateUserStatus,
    DeletePerformerBody,
    DeletePerformerResponse,
    DeletePerformerStatus,
    DeleteUserBody,
    DeleteUserResponse,
    DeleteUserStatus,
    GetMyTasksResponse,
    GetMyTasksStatus,
    GetTasksResponse,
    GetTasksStatus,
    GetUseresStatus,
    GetUserResponse,
    UpdateTaskBody,
    UpdateTaskResponse,
    UpdateTaskStateBody,
    UpdateTaskStateResponse,
    UpdateTaskStateStatus,
    UpdateTaskStatus,
    UpdateUserBody,
    UpdateUserResponse,
    UpdateUserStatus,
    UserProfileResponse,
    UserProfileStatusEnum,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/_internal_/profile", response_model=UserProfileResponse)
async def get_user_profile_info(session: Session = Depends(check_session)):
    """
    Получение данных профиля пользователя.
    """
    user = await app_state.user_repo.get_by_id(user_id=session.user_id)
    if not user:
        return UserProfileResponse(status=UserProfileStatusEnum.user_not_found)

    return UserProfileResponse(
        status=UserProfileStatusEnum.ok,
        username=user.username,
        role=user.role,
        full_name=user.full_name,
    )


@router.get("/_internal_/get_my_tasks", response_model=GetMyTasksResponse)
async def get_my_tasks(session: Session = Depends(check_session)):
    tasks = await app_state.task_repo.get_tasks_by_user(
        user_id=session.user_id
    )
    return GetMyTasksResponse(status=GetMyTasksStatus.ok, tasks=tasks)


@router.get("/_internal_/get_tasks", response_model=GetTasksResponse)
async def get_tasks(session: Session = Depends(check_manager_session)):
    tasks = await app_state.task_repo.get_tasks()
    return GetTasksResponse(status=GetTasksStatus.ok, tasks=tasks)


@router.post("/_internal_/update_user", response_model=UpdateUserResponse)
async def update_user(
    body: UpdateUserBody, session: Session = Depends(check_admin_session)
):
    await app_state.user_repo.update(
        user_id=body.user_id,
        new_role=body.role,
        new_name=body.full_name,
        new_username=body.username,
    )
    return UpdateUserResponse(status=UpdateUserStatus.ok)


@router.get("/_internal_/get_users", response_model=GetUserResponse)
async def get_users(session: Session = Depends(check_manager_session)):
    users = await app_state.user_repo.get_users()
    return GetUserResponse(status=GetUseresStatus.ok, users=users)


@router.post("/_internal_/create_user", response_model=CreateUserResponse)
async def create_user(
    body: CreateUserBody, session: Session = Depends(check_admin_session)
):
    await app_state.user_repo.create(
        username=body.username,
        full_name=body.full_name,
        password_encrypted=get_password_hash(body.password),
        role=body.role,
    )
    return CreateUserResponse(status=CreateUserStatus.ok)


@router.post(
    "/_internal_/change_password", response_model=ChangePasswordResponse
)
async def change_password(
    body: ChangePasswordBody, session: Session = Depends(check_admin_session)
):
    await app_state.user_repo.change_password(
        user_id=body.user_id,
        new_password_encrypted=get_password_hash(body.password),
    )
    return ChangePasswordResponse(status=ChangePasswordStatus.ok)


@router.post("/_internal_/delete_user", response_model=DeleteUserResponse)
async def delete_user(
    body: DeleteUserBody, session: Session = Depends(check_admin_session)
):
    await app_state.user_repo.delete(user_id=body.user_id)
    return DeleteUserResponse(status=DeleteUserStatus.ok)


@router.post("/_internal_/add_preformer", response_model=AddPerformerResponse)
async def add_preformer(
    body: AddPerformerBody, session: Session = Depends(check_manager_session)
):
    await app_state.task_repo.append_performer(
        user_id=body.user_id, task_id=body.task_id
    )
    return AddPerformerResponse(status=AddPerformerStatus.ok)


@router.post(
    "/_internal_/delete_preformer", response_model=DeletePerformerResponse
)
async def delete_preformer(
    body: DeletePerformerBody,
    session: Session = Depends(check_manager_session),
):
    await app_state.task_repo.remove_performer(
        user_id=body.user_id, task_id=body.task_id
    )
    return DeletePerformerResponse(status=DeletePerformerStatus.ok)


@router.post("/_internal_/update_task", response_model=UpdateTaskResponse)
async def update_task(
    body: UpdateTaskBody, session: Session = Depends(check_manager_session)
):
    await app_state.task_repo.update_task(
        task_id=body.task_id,
        new_text=body.text,
        new_caption=body.caption,
        new_state=body.state,
    )
    return UpdateTaskResponse(status=UpdateTaskStatus.ok)


@router.post("/_internal_/create_task", response_model=CreateTaskResponse)
async def create_task(
    body: CreateTaskBody, session: Session = Depends(check_manager_session)
):
    task = await app_state.task_repo.create_task(
        text=body.text,
        caption=body.caption,
        state=body.state,
        created_by=session.user_id,
    )
    for performer_id in body.performers:
        await app_state.task_repo.append_performer(
            task_id=task.id, user_id=performer_id
        )
    return CreateTaskResponse(status=CreateTaskStatus.ok)


@router.post(
    "/_internal_/update_task_state", response_model=UpdateTaskStateResponse
)
async def update_task_state(
    body: UpdateTaskStateBody, session: Session = Depends(check_session)
):
    user = await app_state.user_repo.get_by_id(user_id=session.user_id)
    task = await app_state.task_repo.get_by_id(body.task_id)

    if user.id not in task.performer_id_list:
        return UpdateTaskStateResponse(
            status=UpdateTaskStateStatus.not_enough_rights
        )

    await app_state.task_repo.update_state(
        task_id=body.task_id, new_state=body.new_state
    )

    return UpdateTaskStateResponse(status=UpdateTaskStateStatus.ok)
