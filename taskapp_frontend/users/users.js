async function renderTable(users) {
    document.getElementById('table_container').innerHTML = `
<table>
<thead>
    <tr>
        <th>Имя пользователя</th>
        <th>Полное имя</th>
        <th>Роль</th>
        <th></th>
        <th></th>
        <th>Новый пароль</th>
    </tr>
    </thead>
    <tbody id="user-table-body">
    </tbody>
</table>
`
const userTableBody = document.getElementById("user-table-body");
users.forEach((user) => {
    const row = document.createElement("tr");
    const usernameCell = document.createElement("td");
    const usernameInput = document.createElement("input");
    usernameInput.type = "text";
    usernameInput.value = user.username;
    usernameCell.appendChild(usernameInput);
    row.appendChild(usernameCell);
    const fullNameCell = document.createElement("td");
    const fullNameInput = document.createElement("input");
    fullNameInput.type = "text";
    fullNameInput.value = user.full_name;
    fullNameCell.appendChild(fullNameInput);
    row.appendChild(fullNameCell);
    const roleCell = document.createElement("td");
    const roleSelect = document.createElement("select");
    const roles = [
      { value: 2, text: "Админ" },
      { value: 1, text: "Менеджер" },
      { value: 0, text: "Исполнитель" }
    ];
    roles.forEach((role) => {
      const option = document.createElement("option");
      option.value = role.value;
      option.text = role.text;
      if (role.value === user.role) {
        option.selected = true;
      }
      roleSelect.appendChild(option);
    });
    roleCell.appendChild(roleSelect);
    row.appendChild(roleCell);
    const saveCell = document.createElement("td");
    const saveButton = document.createElement("button");
    saveButton.textContent = "Сохранить";
    saveButton.onclick = () => {
        post('/_internal_/update_user', {
            user_id: user.id,
            username: usernameInput.value,
            full_name: fullNameInput.value,
            role: roleSelect.value
        })
    };
    saveCell.appendChild(saveButton);
    row.appendChild(saveCell);
    const deleteCell = document.createElement("td");
    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Удалить";
    deleteButton.onclick = async () => {
        await post('/_internal_/delete_user', {
            user_id: user.id
        })
        app_state.users = (await get('/_internal_/get_users')).users
        console.log(app_state.users)
        renderTable(app_state.users)
    };
    deleteCell.appendChild(deleteButton);
    row.appendChild(deleteCell);

    const passwordCell = document.createElement("td");
    const passwordInput = document.createElement("input");
    passwordInput.type = "password";
    passwordInput.value = '';
    passwordCell.appendChild(passwordInput);
    row.appendChild(passwordCell);
    const changePasswordCell = document.createElement("td");
    const changePasswordButton = document.createElement("button");
    changePasswordButton.textContent = "Изменить пароль";
    changePasswordButton.onclick = async () => {
      await post('/_internal_/change_password', {
        user_id: user.id,
        password: passwordInput.value
      })
      passwordInput.value = "";
    };
    changePasswordCell.appendChild(changePasswordButton);
    row.appendChild(changePasswordCell);
    userTableBody.appendChild(row);
});
}


async function createUser() {
    await wait_loading()
    const fields = {
        username: document.getElementById('create_username'),
        full_name: document.getElementById('create_full_name'),
        password: document.getElementById('create_password'),
        role: document.getElementById('create_role')
    }
    const new_user = {
        username: fields.username.value,
        full_name: fields.full_name.value,
        password: fields.password.value,
        role: fields.role.value
    }
    Object.values(fields).forEach(field => field.value = '')
    console.log(new_user)
    await post('/_internal_/create_user', new_user)
    app_state.users = (await get('/_internal_/get_users')).users
    console.log(app_state.users)
    renderTable(app_state.users)
}

async function start() {
    await wait_loading()
    app_state.users = (await get('/_internal_/get_users')).users
    console.log(app_state.users)
    renderTable(app_state.users)
}
start()