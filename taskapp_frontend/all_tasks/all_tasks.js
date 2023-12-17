const statusTranslate = {
    not_started: 'Не начато',
    in_progress: 'Выполняется',
    waiting_for_capture: 'Ожидает проверки',
    ended: 'Завершено',
}


async function renderTable(tasks) {
    const taskTableBody = document.getElementById("task-table-body");
    taskTableBody.innerHTML = ''
    tasks.forEach((task) => {
        console.log(task)
        const row = document.createElement("tr");
        
        const captionCell = document.createElement("td");
        const captionP = document.createElement("p");
        captionP.innerHTML = task.caption
        captionCell.appendChild(captionP);
        row.appendChild(captionCell);

        const createdCell = document.createElement("td");
        const createdP = document.createElement("p");
        createdP.innerHTML = task.created_by_name
        createdCell.appendChild(createdP)
        row.appendChild(createdCell)

        const statusCell = document.createElement("td");
        const statusP = document.createElement("p");
        statusP.innerHTML = statusTranslate[task.state]
        statusCell.appendChild(statusP)
        row.appendChild(statusCell)

        const createdAtCell = document.createElement("td");
        const createdAtP = document.createElement("p");
        const created_timestamp = new Date(new Date(task.created_timestamp).getTime() + 3*60*60*1000)
        createdAtP.innerHTML = `${created_timestamp.toLocaleDateString()} ${created_timestamp.toLocaleTimeString()}`
        createdAtCell.appendChild(createdAtP)
        row.appendChild(createdAtCell)

        const editedAtCell = document.createElement("td");
        const editedAtP = document.createElement("p");
        const edited_timestamp = new Date(new Date(task.edited_timestamp).getTime() + 3*60*60*1000)
        editedAtP.innerHTML = `${edited_timestamp.toLocaleDateString()} ${edited_timestamp.toLocaleTimeString()}`
        editedAtCell.appendChild(editedAtP)
        row.appendChild(editedAtCell)

        const performersCell = document.createElement("td");
        task.performer_name_list.forEach(performer => {
            const performerP = document.createElement("p");
            performerP.innerHTML = performer
            performersCell.appendChild(performerP)
        })
        row.appendChild(performersCell)

        const editCell = document.createElement("td");
        const editButton = document.createElement("button");
        editButton.textContent = "Редактировать";
        editButton.onclick = (e) => {
            e.preventDefault()
            renderEdit(task)
        };
        editCell.appendChild(editButton);
        row.appendChild(editCell);
        
        taskTableBody.appendChild(row)
    })
}

async function renderEdit(task) {
    console.log(task)
    app_state.selected_task = task

    const caption = document.getElementById('edit_caption')
    const text = document.getElementById('edit_text')
    const state = document.getElementById('edit_state')
    const table = document.getElementById('edit-task-performers-table-body')

    table.innerHTML = ''

    caption.value = task.caption
    text.value = task.text
    state.value = task.state
    
    for (let i = 0; i < task.performer_name_list.length; i++) {
        const name = task.performer_name_list[i]
        const user_id = task.performer_id_list[i]
        console.log(name, user_id)
        const row = document.createElement("tr")
        
        const nameCell = document.createElement("td")
        const nameP = document.createElement("p")
        nameP.innerHTML = name
        nameCell.appendChild(nameP);
        row.appendChild(nameCell);

        const deleteCell = document.createElement("td");
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Удалить";
        deleteButton.onclick = async (e) => {
            e.preventDefault()
            task.performer_id_list.splice(i, 1)
            task.performer_name_list.splice(i, 1)
            await post("/_internal_/delete_preformer", {
                user_id: user_id,
                task_id: task.id
            })
            renderEdit(task)
            renderTable(app_state.tasks)
        };
        deleteCell.appendChild(deleteButton);
        row.appendChild(deleteCell);

        table.appendChild(row)
    }
    const row = document.createElement("tr")
    const select = document.createElement("select")
    app_state.users.forEach(user => {
        const option = document.createElement("option")
        option.value = user.id
        option.innerHTML = user.full_name
        select.appendChild(option)
    })
    row.appendChild(select)
    const addCell = document.createElement("td");
    const addButton = document.createElement("button");
    addButton.textContent = "Добавить";
    addButton.onclick = async (e) => {
        e.preventDefault()
        const user_id = select.value
        const name = app_state.users.find(user => { return user_id == user.id}).full_name
        const task_id = task.id
        console.log(name, user_id, task_id)
        await post("/_internal_/add_preformer", {
            user_id: user_id,
            task_id: task_id
        })
        
        task.performer_name_list.push(name)
        task.performer_id_list.push(user_id)
        renderEdit(task)
        renderTable(app_state.tasks)
    };
    addCell.appendChild(addButton);
    row.appendChild(addCell);
    table.appendChild(row)
}


async function saveTask() {
    const task = app_state.selected_task

    const caption = document.getElementById('edit_caption')
    const text = document.getElementById('edit_text')
    const state = document.getElementById('edit_state')

    task.caption = caption.value
    task.text = text.value
    task.state = state.value
    task.edited_timestamp = new Date(Date.now() - 60*60*3*1000)

    await post('/_internal_/update_task', {
        caption: caption.value,
        text: text.value,
        state: state.value,
        task_id: task.id
    })
    
    caption.value = ''
    text.value = ''
    state.value = ''
    const table = document.getElementById('edit-task-performers-table-body')
    table.innerHTML = ''
    app_state.selected_task = null
    renderTable(app_state.tasks)
}


async function renderCreate(creatingTask = null) {
    const caption = document.getElementById('create_caption')
    const text = document.getElementById('create_text')
    const state = document.getElementById('create_state')
    const table = document.getElementById('create-task-performers-table-body')

    table.innerHTML = ''

    if (!creatingTask)
        app_state.creatingTask = {
            caption: caption.value,
            text: text.value,
            state: state.value,
            performer_name_list: [],
            performer_id_list: [],
            created_by: app_state.user_info.id,
            created_by_name: app_state.user_info.full_name
        }
    else
        app_state.creatingTask = creatingTask


    
    for (let i = 0; i < app_state.creatingTask.performer_name_list.length; i++) {
        const name = app_state.creatingTask.performer_name_list[i]
        const user_id = app_state.creatingTask.performer_id_list[i]
        console.log(name, user_id)
        const row = document.createElement("tr")
        
        const nameCell = document.createElement("td")
        const nameP = document.createElement("p")
        nameP.innerHTML = name
        nameCell.appendChild(nameP);
        row.appendChild(nameCell);

        const deleteCell = document.createElement("td");
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Удалить";
        deleteButton.onclick = async (e) => {
            e.preventDefault()
            app_state.creatingTask.performer_id_list.splice(i, 1)
            app_state.creatingTask.performer_name_list.splice(i, 1)
            renderCreate(app_state.creatingTask)
        };
        deleteCell.appendChild(deleteButton);
        row.appendChild(deleteCell);

        table.appendChild(row)
    }
    const row = document.createElement("tr")
    const select = document.createElement("select")
    app_state.users.forEach(user => {
        const option = document.createElement("option")
        option.value = user.id
        option.innerHTML = user.full_name
        select.appendChild(option)
    })
    row.appendChild(select)
    const addCell = document.createElement("td");
    const addButton = document.createElement("button");
    addButton.textContent = "Добавить";
    addButton.onclick = async (e) => {
        e.preventDefault()
        const user_id = select.value
        const name = app_state.users.find(user => { return user_id == user.id}).full_name
        
        app_state.creatingTask.performer_name_list.push(name)
        app_state.creatingTask.performer_id_list.push(user_id)
        renderCreate(app_state.creatingTask)
    };
    addCell.appendChild(addButton);
    row.appendChild(addCell);
    table.appendChild(row)
}

async function createTask() {
    const task = app_state.creatingTask

    const caption = document.getElementById('create_caption')
    const text = document.getElementById('create_text')
    const state = document.getElementById('create_state')

    task.caption = caption.value
    task.text = text.value
    task.state = state.value
    task.edited_timestamp = new Date(Date.now() - 60*60*3*1000)
    task.created_timestamp = new Date(Date.now() - 60*60*3*1000)

    await post('/_internal_/create_task', {
        caption: task.caption,
        text: task.text,
        state: task.state,
        performers: task.performer_id_list
    })
    
    caption.value = ''
    text.value = ''
    state.value = ''
    const table = document.getElementById('edit-task-performers-table-body')
    table.innerHTML = ''
    
    app_state.tasks.push(task)
    renderTable(app_state.tasks)
    app_state.creatingTask = null
}

async function start() {
    await wait_loading()
    app_state.tasks = (await get('/_internal_/get_tasks')).tasks
    app_state.users = (await get('/_internal_/get_users')).users
    console.log(app_state.tasks)
    renderTable(app_state.tasks)
    renderCreate()
}
start()