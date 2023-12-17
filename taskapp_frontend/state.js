async function wait(ms=100) {
    return new Promise((res, rej) => {
        setTimeout(res,ms)
    })
}

async function wait_loading() {
    while(true) {
        if (app_state.ready) break
        else await wait(100)
    }
    console.log('Состояние загружено', app_state)
    return true
}

async function get(url, params = {}, other = {}) {
    return new Promise((res,rej) => {
        fetch(url + '?' + new URLSearchParams(params).toString(), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            ...other
        }).then((response) => { res(response.json()) }).catch((error) => {rej(error)})
    })
}

async function post(url, body = {}, params = {}, other = {}) {
    return new Promise((res,rej) => {
        fetch(url + '?' + new URLSearchParams(params).toString(), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body),
            ...other
        }).then((response) => { res(response.json()) }).catch((error) => {rej(error)})
    })
}

function createNavbar(navItems, username) {
    document.getElementById('navbar').innerHTML = `
    <h1>Распределение задач</h1>
    <nav>
        <ul>
            <div id="user-info">
                <p><span id="username"></span></p>
                <button onclick="logout()">Выйти</button>
            </div>
        </ul>
    </nav>
    `
    const nav = document.querySelector('nav ul');
    const usernameEl = document.querySelector('#username');

    navItems.forEach(item => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = item.url;
    a.textContent = item.text;
    li.appendChild(a);
    nav.prepend(li);
    });

    usernameEl.textContent = username;
}

async function logout() {
    await post('/_internal_/logout')
    window.location.reload()
}

const app_state = {}
async function load_state() {
    app_state.ready = false
    app_state.user_info = await get('/_internal_/profile')
    console.log(app_state.user_info)
    const nav_roles = [
        [{url: '/my_tasks/', text: 'Мои задачи'}],
        [{url: '/my_tasks/', text: 'Мои задачи'}, {url: '/all_tasks/', text: 'Все задачи'}],
        [{url: '/my_tasks/', text: 'Мои задачи'}, {url: '/all_tasks/', text: 'Все задачи'}, {url: '/users/', text: 'Пользователи'}],
    ]

    const role_views = nav_roles[app_state.user_info.role]
    const can_access = role_views.find(view => { return view.url == window.location.pathname})
    if (!can_access && window.location.pathname != '/')
        window.location.href = '/'

    createNavbar(role_views, app_state.user_info.full_name)
    app_state.ready = true
}
load_state()
