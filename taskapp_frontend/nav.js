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