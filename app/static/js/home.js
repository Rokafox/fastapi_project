

// ページのスクロール位置を保存する
window.addEventListener("beforeunload", function() {
    localStorage.setItem("scrollPosition", window.scrollY);
});

// ページのスクロール位置を復元する
window.addEventListener("load", function() {
    const scrollPosition = localStorage.getItem("scrollPosition");
    if (scrollPosition) {
        window.scrollTo(0, parseInt(scrollPosition));
    }
});

// ユーザー名とプロジェクト名のドロップダウンを作成
document.addEventListener("DOMContentLoaded", function() {
    fetch('/users_hiruchaaru')
    .then(response => response.json())
    .then(users => {
        users.forEach(user => {
            const option = document.createElement('option');
            option.value = user.name;
            option.textContent = user.name;
            option.dataset.password = user.password;
            option.dataset.role = user.role;
            document.getElementById('pmasu_the_user_name').appendChild(option);
            //pmuasu_the_user_name
            document.getElementById('pmuasu_the_user_name').appendChild(option.cloneNode(true));
        });

    })
    .catch(error => console.error('Error fetching users:', error));

    // プロジェクトの情報を取得してドロップダウンに追加
    fetch(`/projects_pm/${current_user_name}`)
    .then(response => response.json())
    .then(projects => {
        projects.forEach(project => {
            const option = document.createElement('option');
            option.value = project.name;
            option.textContent = project.name;
            document.getElementById('pmasu_the_project_name').appendChild(option);
            //pmuasu_the_project_name
            document.getElementById('pmuasu_the_project_name').appendChild(option.cloneNode(true));
            //pmcreatetask_the_project_name
            document.getElementById('pmcreatetask_the_project_name').appendChild(option.cloneNode(true));
        });
    })
    .catch(error => console.error('Error fetching projects:', error));
});


// ユーザーのラジオボタンを動的に作成
document.addEventListener("DOMContentLoaded", async function() {
    const userSelectionDiv = document.getElementById("pmcreatetask_the_user_names");
    const userListInput = document.getElementById("pmcreatetask_user_list");

    // ユーザーリストを取得する関数
    async function fetchUsers() {
        const response = await fetch('/users_hiruchaaru');
        const users = await response.json();
        return users;
    }

    // ユーザーのチェックボックスを動的に作成
    function createCheckboxes(users) {
        users.forEach(user => {
            const label = document.createElement('label');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = user.name;
            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(user.name));
            userSelectionDiv.appendChild(label);
        });
    }

    // フォーム送信前にチェックボックスの選択状態を処理
    document.getElementById('pmcreateTaskForm').addEventListener('submit', function(event) {
        const selectedUsers = [];
        const checkboxes = userSelectionDiv.querySelectorAll('input[type="checkbox"]:checked');
        checkboxes.forEach(checkbox => {
            selectedUsers.push(checkbox.value);
        });

        // 選択されたユーザー名をカンマ区切りで入力値に設定
        userListInput.value = selectedUsers.join(',');
        // We are not allowed to send null, so we send an empty string instead
        if (userListInput.value === '') {
            userListInput.value = '';
        }
    });

    // ユーザーリストを取得し、チェックボックスを生成
    const users = await fetchUsers();
    createCheckboxes(users);
});
