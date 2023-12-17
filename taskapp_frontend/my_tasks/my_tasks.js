const statusTranslate = {
    not_started: 'Не начато',
    in_progress: 'Выполняется',
    waiting_for_capture: 'Ожидает проверки',
    ended: 'Завершено',
}

function prettyfiy_date(date_str) {
    const date = new Date(new Date(date_str).getTime() + 3*60*60*1000)
    const result = `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`  
    return result
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
        createdAtP.innerHTML = prettyfiy_date(task.created_timestamp)
        createdAtCell.appendChild(createdAtP)
        row.appendChild(createdAtCell)

        const editedAtCell = document.createElement("td");
        const editedAtP = document.createElement("p");
        editedAtP.innerHTML = prettyfiy_date(task.edited_timestamp)
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
        editButton.textContent = "Просмотр";
        editButton.onclick = (e) => {
            e.preventDefault()
            renderView(task)
        };
        editCell.appendChild(editButton);
        row.appendChild(editCell);
        
        taskTableBody.appendChild(row)
    })
}

async function renderView(task) {
    console.log(task)
    app_state.selected_task = task

    const caption = document.getElementById('view_caption')
    const text = document.getElementById('view_text')
    const state = document.getElementById('view_state')
    const dates = document.getElementById('view_dates')
    const table = document.getElementById('view-task-performers-table-body')


    table.innerHTML = ''

    caption.innerHTML = task.caption
    text.innerHTML = task.text
    state.value = task.state
    dates.innerHTML = `<b>Создано</b>: ${prettyfiy_date(task.created_timestamp)}<br><b>Изменено</b>: ${prettyfiy_date(task.edited_timestamp)}`
    
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
        table.appendChild(row)
    }
}

async function saveTask() {
    const task = app_state.selected_task
    const state = document.getElementById('view_state')

    task.state = state.value
    task.edited_timestamp = new Date(Date.now() - 60*60*3*1000)

    await post('/_internal_/update_task_state', {
        new_state: state.value,
        task_id: task.id
    })
    
    renderTable(app_state.tasks)
}


async function start() {
    await wait_loading()
    app_state.tasks = (await get('/_internal_/get_my_tasks')).tasks
    console.log(app_state.tasks)
    renderTable(app_state.tasks)
}
start()