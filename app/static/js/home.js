

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

            // 各要素が存在するか確認してから追加
            const pmasuUserElement = document.getElementById('pmasu_the_user_name');
            if (pmasuUserElement) {
                pmasuUserElement.appendChild(option.cloneNode(true));
            }

            const pmuasuUserElement = document.getElementById('pmuasu_the_user_name');
            if (pmuasuUserElement) {
                pmuasuUserElement.appendChild(option.cloneNode(true));
            }
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

            // 各要素が存在するか確認してから追加
            const pmasuElement = document.getElementById('pmasu_the_project_name');
            if (pmasuElement) {
                pmasuElement.appendChild(option.cloneNode(true));
            }

            const pmuasuElement = document.getElementById('pmuasu_the_project_name');
            if (pmuasuElement) {
                pmuasuElement.appendChild(option.cloneNode(true));
            }

            const pmcreatetaskElement = document.getElementById('pmcreatetask_the_project_name');
            if (pmcreatetaskElement) {
                pmcreatetaskElement.appendChild(option.cloneNode(true));
            }
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
    pmcreatetaskFormElement = document.getElementById('pmcreateTaskForm');
    if (pmcreatetaskFormElement) {
        pmcreatetaskFormElement.addEventListener('submit', function(event) {
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
    }

    // ユーザーリストを取得し、チェックボックスを生成
    // if userSelectionDiv and userListInput exist
    if (userSelectionDiv && userListInput) {
        const users = await fetchUsers();
        createCheckboxes(users);
    }
});







let hiruchaaru_attendances = [];
            
try {
    document.getElementById('hrc_show-attendances-btn').addEventListener('click', () => {
        hrc_fetchAttendances();
        document.getElementById('filter-input').style.display = 'block';
        document.getElementById('attendance-list').style.display = 'block';
        document.getElementById('hrc_show-attendances-btn').style.display = 'none';
        document.getElementById('hrc_hide-attendances-btn').style.display = 'block';
    });
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('hrc_hide-attendances-btn').addEventListener('click', () => {
        document.getElementById('filter-input').style.display = 'none';
        document.getElementById('attendance-list').style.display = 'none';
        document.getElementById('hrc_hide-attendances-btn').style.display = 'none';
        document.getElementById('hrc_show-attendances-btn').style.display = 'block';
    });
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('filter-input').addEventListener('input', hrc_filterAttendances);
} catch (error) {
    console.log(error);
}

async function hrc_fetchAttendances() {
    const response = await fetch(`/attendances/${current_user_name}`);
    hiruchaaru_attendances = await response.json();
    hrc_displayAttendances(hiruchaaru_attendances);
}

function hrc_displayAttendances(attendanceList) {
    const attendanceListElement = document.getElementById('attendance-list');
    attendanceListElement.innerHTML = '';

    attendanceList.forEach(attendance => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <strong>Project:</strong> ${attendance.project_name} <br>
            <strong>Scheduled Starttime:</strong> ${attendance.project_starttime} <br>
            <strong>Scheduled Endtime:</strong> ${attendance.project_endtime} <br>
            <strong>Date:</strong> ${attendance.date} <br>
            <strong>Check In:</strong> ${attendance.check_in ? attendance.check_in : 'Not checked in yet'} <br>
            <strong>Check Out:</strong> ${attendance.check_out ? attendance.check_out : 'Not checked out yet'} <br>
        `;

        // Check In ボタン（check_in が存在しない場合のみ表示）
        if (!attendance.check_in) {
            const checkInButton = document.createElement('button');
            checkInButton.textContent = 'Check In';
            checkInButton.style = "background-color: #333; border: none; color: white; padding: 9px 30px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px;";
            checkInButton.onclick = () => hrc_checkIn(attendance.id);
            listItem.appendChild(checkInButton);
        }

        // Check Out ボタン（check_in が存在し、かつ check_out が存在しない場合のみ表示）
        if (attendance.check_in && !attendance.check_out) {
            const checkOutButton = document.createElement('button');
            checkOutButton.textContent = 'Check Out';
            checkOutButton.style = "background-color: #333; border: none; color: white; padding: 9px 30px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px;";
            checkOutButton.onclick = () => hrc_checkOut(attendance.id);
            listItem.appendChild(checkOutButton);
        }

        attendanceListElement.appendChild(listItem);
    });
}

async function hrc_checkIn(attendanceId) {
    const response = await fetch(`/attendances/${attendanceId}/checkin`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: ''
    });
    const response_result = await response.json();

    if (response_result.success) {
        alert('Successfully checked in!');
        hrc_fetchAttendances(); // 再読み込みしてリストを更新
    } else {
        alert('Failed to check in');
    }
}

async function hrc_checkOut(attendanceId) {
    const response = await fetch(`/attendances/${attendanceId}/checkout`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: ''
    });
    const response_result = await response.json();

    if (response_result.success) {
        alert('Successfully checked out!');
        hrc_fetchAttendances(); // 再読み込みしてリストを更新
    } else {
        alert('Failed to check out');
    }
}

function hrc_filterAttendances() {
    const filterValue = document.getElementById('filter-input').value.toLowerCase();
    const filteredAttendances = hiruchaaru_attendances.filter(attendance => 
        attendance.project_name.toLowerCase().includes(filterValue) ||
        attendance.project_starttime.toLowerCase().includes(filterValue) ||
        attendance.project_endtime.toLowerCase().includes(filterValue) ||
        attendance.date.toLowerCase().includes(filterValue)
    );
    hrc_displayAttendances(filteredAttendances);
}











let hrctasks = [];
            
try {
    document.getElementById('hrctsk-show-tasks-btn').addEventListener('click', () => {
        hrc_fetchTasks();
        document.getElementById('hrctsk-filter-input').style.display = 'block';
        document.getElementById('hrctsk-task-list').style.display = 'block';
        document.getElementById('hrctsk-show-tasks-btn').style.display = 'none';
        document.getElementById('hrctsk-hide-tasks-btn').style.display = 'block';
    });
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('hrctsk-hide-tasks-btn').addEventListener('click', () => {
        document.getElementById('hrctsk-filter-input').style.display = 'none';
        document.getElementById('hrctsk-task-list').style.display = 'none';
        document.getElementById('hrctsk-hide-tasks-btn').style.display = 'none';
        document.getElementById('hrctsk-show-tasks-btn').style.display = 'block';
    });
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('hrctsk-filter-input').addEventListener('input', hrc_filterTasks);
} catch (error) {
    console.log(error);
}

async function hrc_fetchTasks() {
    const response = await fetch(`/tasks_for_specific_hiruchaaru/${current_user_name}`);
    hrctasks = await response.json();
    hrc_displayTasks(hrctasks);
}

function hrc_displayTasks(taskList) {
    const taskListElement = document.getElementById('hrctsk-task-list');
    taskListElement.innerHTML = '';

    taskList.forEach(task => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <strong>Project:</strong> ${task.project_name} <br>
            <strong>Start Date:</strong> ${task.start_date} <br>
            <strong>End Date:</strong> ${task.end_date} <br>
            <strong>Description:</strong> ${task.status} <br>
            <strong>Progress:</strong> ${task.progress}% <br>
        `;
        // task_assigned_for_this_user が True の場合のみ「Edit」ボタンを表示
        if (task.task_assigned_for_this_user) {
            listItem.innerHTML += `
                <button style="background-color: #333; border: none; color: white; padding: 9px 30px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px;" onclick="hrc_editTask(${task.id})">Edit</button>
            `;
        }
        taskListElement.appendChild(listItem);
    });
}

function hrc_filterTasks() {
    const filterValue = document.getElementById('hrctsk-filter-input').value.toLowerCase();
    const filteredTasks = hrctasks.filter(task => 
        task.project_name.toLowerCase().includes(filterValue) ||
        task.start_date.toLowerCase().includes(filterValue) ||
        task.end_date.toLowerCase().includes(filterValue) ||
        (task.status && task.status.toLowerCase().includes(filterValue))
    );
    hrc_displayTasks(filteredTasks);
}

async function hrc_editTask(taskId) {
    const task = hrctasks.find(t => t.id === taskId);

    // document.getElementById('hrctsk-edit-status').value = task.status || '';
    document.getElementById('hrctsk-edit-task-progress').value = task.progress;

    document.getElementById('hrctsk-edit-task-modal').style.display = 'block';

    document.getElementById('hrctsk-edit-task-form').onsubmit = async (e) => {
        e.preventDefault();

        const updatedTask = {
            // status: document.getElementById('hrctsk-edit-status').value,
            progress: document.getElementById('hrctsk-edit-task-progress').value,
        };

        const response = await fetch(`/tasks/${taskId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedTask),
        });

        const response_result = await response.json();
        if (response_result.success) {
            hrc_fetchTasks();
            document.getElementById('hrctsk-edit-task-modal').style.display = 'none';
        } else {
            alert('Failed to update task: ' + response_result.message);
        }
    };

    document.getElementById('hrctsk-cancel-edit').addEventListener('click', () => {
        document.getElementById('hrctsk-edit-task-modal').style.display = 'none';
    });
}












let pmv_projects = [];
            
try {
    document.getElementById('show-projects-btn').addEventListener('click', () => {
        pmv_fetchProjects();
        document.getElementById('filter-input').style.display = 'block';
        document.getElementById('project-list').style.display = 'block';
        document.getElementById('show-projects-btn').style.display = 'none';
        document.getElementById('hide-projects-btn').style.display = 'block';
    });
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('hide-projects-btn').addEventListener('click', () => {
        document.getElementById('filter-input').style.display = 'none';
        document.getElementById('project-list').style.display = 'none';
        document.getElementById('hide-projects-btn').style.display = 'none';
        document.getElementById('show-projects-btn').style.display = 'block';
    });
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('filter-input').addEventListener('input', pmv_filterProjects);
} catch (error) {
    console.log(error);
}

async function pmv_fetchProjects() {
    const response = await fetch(`/projects_pm/${current_user_name}`);
    pmv_projects = await response.json();
    pmv_displayProjects(pmv_projects);
}

function pmv_displayProjects(projectList) {
    const projectListElement = document.getElementById('project-list');
    projectListElement.innerHTML = ''; // リストをクリア

    projectList.forEach(project => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <strong>Name:</strong> ${project.name} <br>
            <strong>Description:</strong> ${project.description} <br>
            <strong>Start Time:</strong> ${project.starttime} <br>
            <strong>End Time:</strong> ${project.endtime} <br>
            <strong>Status:</strong> ${project.status} <br>
            <button style="background-color: #333; border: none; color: white; padding: 9px 30px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px;" onclick="pmv_editProject(${project.id})">Edit</button>
            <button style="background-color: #333; border: none; color: white; padding: 9px 30px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px;" onclick="pmv_deleteProject(${project.id})">Delete</button>
        `;
        projectListElement.appendChild(listItem);
    });
}

function pmv_filterProjects() {
    const filterValue = document.getElementById('filter-input').value.toLowerCase();
    const filteredProjects = pmv_projects.filter(project => 
        project.name.toLowerCase().includes(filterValue) ||
        project.description.toLowerCase().includes(filterValue) ||
        project.starttime.toLowerCase().includes(filterValue) ||
        project.endtime.toLowerCase().includes(filterValue) ||
        project.status.toLowerCase().includes(filterValue)
    );
    pmv_displayProjects(filteredProjects);
}

async function pmv_editProject(projectId) {
    // 選択したプロジェクトのデータを取得
    const project = pmv_projects.find(p => p.id === projectId);

    // フォームにプロジェクトのデータをセット
    document.getElementById('edit-name').value = project.name;
    document.getElementById('edit-description').value = project.description;
    document.getElementById('edit-starttime').value = project.starttime;
    document.getElementById('edit-endtime').value = project.endtime;
    document.getElementById('edit-status').value = project.status;

    // 編集モーダルを表示
    document.getElementById('edit-project-modal').style.display = 'block';

    // フォームのサブミット処理
    document.getElementById('edit-project-form').onsubmit = async (e) => {
        e.preventDefault();

        // フォームからデータを取得
        const updatedProject = {
            name: document.getElementById('edit-name').value,
            description: document.getElementById('edit-description').value,
            starttime: document.getElementById('edit-starttime').value.replace('T', ' '),
            endtime: document.getElementById('edit-endtime').value.replace('T', ' '),
            status: document.getElementById('edit-status').value,
        };

        // サーバーにPATCHリクエストを送信
        const response = await fetch(`/projects/${projectId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedProject),
        });

        const response_result = await response.json();
        if (response_result.success) {
            pmv_fetchProjects();
            // モーダルを非表示
            document.getElementById('edit-project-modal').style.display = 'none';
        } else {
            alert('Failed to update project: ' + response_result.message);  // エラーメッセージを表示
        }

    };

    // キャンセルボタンの処理
    document.getElementById('cancel-edit').addEventListener('click', () => {
        document.getElementById('edit-project-modal').style.display = 'none';
    });
}


async function pmv_deleteProject(projectId) {
    const confirmation = confirm(`Are you sure you want to delete this project?`);
    if (!confirmation) {
        return;
    }

    try {
        const response = await fetch(`/projects/${projectId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const response_result = await response.json();

        if (response_result.success) {
            pmv_fetchProjects();
        } else {
            const errorData = await response.json();
            alert(`Failed to delete project: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Error deleting project:', error);
        alert('An error occurred while deleting the project.');
    }
}













let pmv_attendances = [];

try {
    document.getElementById('pmat_show-attendances-btn').addEventListener('click', () => {
        pmv_fetchAttendances();
        document.getElementById('attendance-and-filterA').style.display = 'block';
        document.getElementById('attendance-and-filterB').style.display = 'block';
        document.getElementById('attendance-and-filterC').style.display = 'block';
        document.getElementById('attendance-filter-date-before').style.display = 'block'; // date beforeフィルター
        document.getElementById('attendance-filter-date-after').style.display = 'block'; // date afterフィルター
        document.getElementById('attendance-list').style.display = 'block';
        document.getElementById('calculate-btn').style.display = 'block';
        document.getElementById('pmat_show-attendances-btn').style.display = 'none';
        document.getElementById('pmat_hide-attendances-btn').style.display = 'block';
    });
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('pmat_hide-attendances-btn').addEventListener('click', () => {
        document.getElementById('attendance-and-filterA').style.display = 'none';
        document.getElementById('attendance-and-filterB').style.display = 'none';
        document.getElementById('attendance-and-filterC').style.display = 'none';
        document.getElementById('attendance-filter-date-before').style.display = 'none'; // date beforeフィルター
        document.getElementById('attendance-filter-date-after').style.display = 'none'; // date afterフィルター
        document.getElementById('attendance-list').style.display = 'none';
        document.getElementById('calculate-btn').style.display = 'none';
        document.getElementById('pmat_hide-attendances-btn').style.display = 'none';
        document.getElementById('pmat_show-attendances-btn').style.display = 'block';
        document.getElementById('calculate-output').style.display = 'none';
    });
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('attendance-and-filterA').addEventListener('input', pmv_filterAttendances);
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('attendance-and-filterB').addEventListener('input', pmv_filterAttendances);
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('attendance-and-filterC').addEventListener('input', pmv_filterAttendances);
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('attendance-filter-date-before').addEventListener('input', pmv_filterAttendances); // date before
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('attendance-filter-date-after').addEventListener('input', pmv_filterAttendances);  // date after
} catch (error) {
    console.log(error);
}

async function pmv_fetchAttendances() {
    const response = await fetch('/attendances');
    pmv_attendances = await response.json();
    pmv_displayAttendances(pmv_attendances);
}

function pmv_displayAttendances(attendanceList) {
    const attendanceListElement = document.getElementById('attendance-list');
    attendanceListElement.innerHTML = ''; // リストをクリア

    attendanceList.forEach(attendance => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <strong>User Name:</strong> ${attendance.user_name} <br>
            <strong>Project Name:</strong> ${attendance.project_name} <br>
            <strong>Scheduled Date:</strong> ${attendance.date} <br>
            <strong>Scheduled Starttime:</strong> ${attendance.project_starttime} <br>
            <strong>Scheduled Endtime:</strong> ${attendance.project_endtime} <br>
            <strong>Check In:</strong> ${attendance.check_in} <br>
            <strong>Check Out:</strong> ${attendance.check_out} <br>
        `;
        attendanceListElement.appendChild(listItem);
    });
}

function pmv_filterAttendances() {
    const filterValueA = document.getElementById('attendance-and-filterA').value.toLowerCase();
    const filterValueB = document.getElementById('attendance-and-filterB').value.toLowerCase();
    const filterValueC = document.getElementById('attendance-and-filterC').value.toLowerCase();
    const dateBefore = new Date(document.getElementById('attendance-filter-date-before').value);
    const dateAfter = new Date(document.getElementById('attendance-filter-date-after').value);

    // フィルターAを適用
    let filteredAttendances = pmv_attendances.filter(attendance => 
        attendance.user_name.toLowerCase().includes(filterValueA) ||
        attendance.project_name.toLowerCase().includes(filterValueA) ||
        attendance.date.toLowerCase().includes(filterValueA)
    );

    // フィルターBを適用
    filteredAttendances = filteredAttendances.filter(attendance => 
        attendance.user_name.toLowerCase().includes(filterValueB) ||
        attendance.project_name.toLowerCase().includes(filterValueB) ||
        attendance.date.toLowerCase().includes(filterValueB)
    );

    // フィルターCを適用
    filteredAttendances = filteredAttendances.filter(attendance => 
        attendance.user_name.toLowerCase().includes(filterValueC) ||
        attendance.project_name.toLowerCase().includes(filterValueC) ||
        attendance.date.toLowerCase().includes(filterValueC)
    );

    // date beforeフィルターを適用
    if (!isNaN(dateBefore.getTime())) {  // 有効な日付か確認
        filteredAttendances = filteredAttendances.filter(attendance => {
            const attendanceDate = new Date(attendance.date);
            return attendanceDate <= dateBefore;
        });
    }

    // date afterフィルターを適用
    if (!isNaN(dateAfter.getTime())) {  // 有効な日付か確認
        filteredAttendances = filteredAttendances.filter(attendance => {
            const attendanceDate = new Date(attendance.date);
            return attendanceDate >= dateAfter;
        });
    }

    // 絞り込んだ結果を表示
    pmv_displayAttendances(filteredAttendances);
}

try {
    document.getElementById('calculate-btn').addEventListener('click', () => {
        pmv_calculateAttendanceRate();
        document.getElementById('calculate-output').style.display = 'block';
    });
} catch (error) {
    console.log(error);
}

function pmv_calculateAttendanceRate() {
    const filterValueA = document.getElementById('attendance-and-filterA').value.toLowerCase();
    const filterValueB = document.getElementById('attendance-and-filterB').value.toLowerCase();
    const filterValueC = document.getElementById('attendance-and-filterC').value.toLowerCase();
    const dateBefore = new Date(document.getElementById('attendance-filter-date-before').value);
    const dateAfter = new Date(document.getElementById('attendance-filter-date-after').value);

    const filteredAttendancesA = pmv_attendances.filter(attendance => 
        attendance.user_name.toLowerCase().includes(filterValueA) ||
        attendance.project_name.toLowerCase().includes(filterValueA) ||
        attendance.date.toLowerCase().includes(filterValueA)
    );

    const filteredAttendancesB = filteredAttendancesA.filter(attendance => 
        attendance.user_name.toLowerCase().includes(filterValueB) ||
        attendance.project_name.toLowerCase().includes(filterValueB) ||
        attendance.date.toLowerCase().includes(filterValueB)
    );

    let filteredAttendancesC = filteredAttendancesB.filter(attendance => 
        attendance.user_name.toLowerCase().includes(filterValueC) ||
        attendance.project_name.toLowerCase().includes(filterValueC) ||
        attendance.date.toLowerCase().includes(filterValueC)
    );

    // date beforeフィルターを適用
    if (!isNaN(dateBefore.getTime())) {  // 有効な日付か確認
        filteredAttendancesC = filteredAttendancesC.filter(attendance => {
            const attendanceDate = new Date(attendance.date);
            return attendanceDate <= dateBefore;
        });
    }

    // date afterフィルターを適用
    if (!isNaN(dateAfter.getTime())) {  // 有効な日付か確認
        filteredAttendancesC = filteredAttendancesC.filter(attendance => {
            const attendanceDate = new Date(attendance.date);
            return attendanceDate >= dateAfter;
        });
    }

    let outputText = "";
    let totalRate = 0;
    let validCount = 0; // 有効な出席レートの数

    filteredAttendancesC.forEach(attendance => {
        const scheduledStart = new Date(`1970-01-01T${attendance.project_starttime}:00`);
        const scheduledEnd = new Date(`1970-01-01T${attendance.project_endtime}:00`);
        const checkIn = new Date(`1970-01-01T${attendance.check_in}:00`);
        const checkOut = new Date(`1970-01-01T${attendance.check_out}:00`);

        const scheduledTime = (scheduledEnd - scheduledStart) / (1000 * 60); // スケジュールされた時間 (分)
        const actualTime = (checkOut - checkIn) / (1000 * 60); // 実際の働いた時間 (分)

        let attendanceRate = 0;
        if (scheduledTime > 0) {
            attendanceRate = (actualTime / scheduledTime) * 100; // 出席率 (パーセンテージ)
        }

        totalRate += attendanceRate;
        validCount++; // 有効な出席の数を増加

        outputText += `<strong>${attendance.user_name} - ${attendance.project_name} - ${attendance.date}:</strong> Attendance Rate: ${attendanceRate.toFixed(2)}%<br>`;
    });

    // 出席率の平均を計算
    let averageRate = validCount > 0 ? (totalRate / validCount).toFixed(2) : 0;

    // 平均出席率を追加
    outputText += `<br><strong>Average Attendance Rate:</strong> ${averageRate}%`;

    document.getElementById('calculate-output').innerHTML = outputText;
}
















let pmvtasks = [];
            
try {
    document.getElementById('pmtsk-show-tasks-btn').addEventListener('click', () => {
        pmv_fetchTasks();
        document.getElementById('pmtsk-filter-input').style.display = 'block';
        document.getElementById('pmtsk-task-list').style.display = 'block';
        document.getElementById('pmtsk-show-tasks-btn').style.display = 'none';
        document.getElementById('pmtsk-hide-tasks-btn').style.display = 'block';
    });
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('pmtsk-hide-tasks-btn').addEventListener('click', () => {
        document.getElementById('pmtsk-filter-input').style.display = 'none';
        document.getElementById('pmtsk-task-list').style.display = 'none';
        document.getElementById('pmtsk-hide-tasks-btn').style.display = 'none';
        document.getElementById('pmtsk-show-tasks-btn').style.display = 'block';
    });
} catch (error) {
    console.log(error);
}

try {
    document.getElementById('pmtsk-filter-input').addEventListener('input', pmv_filterTasks);
} catch (error) {
    console.log(error);
}

async function pmv_fetchTasks() {
    const response = await fetch(`/tasks`);
    pmvtasks = await response.json();
    pmv_displayTasks(pmvtasks);
}

function pmv_displayTasks(taskList) {
    const taskListElement = document.getElementById('pmtsk-task-list');
    taskListElement.innerHTML = ''; // リストをクリア

    taskList.forEach(task => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <strong>Project:</strong> ${task.project_name} <br>
            <strong>User:</strong> ${task.user_names} <br>
            <strong>Start Date:</strong> ${task.start_date} <br>
            <strong>End Date:</strong> ${task.end_date} <br>
            <strong>Description:</strong> ${task.status} <br>
            <strong>Progress:</strong> ${task.progress}% <br>
            <button style="background-color: #333; border: none; color: white; padding: 9px 30px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px;" onclick="pmv_editTask(${task.id})">Edit</button>
            <button style="background-color: #333; border: none; color: white; padding: 9px 30px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px;" onclick="pmv_deleteTask(${task.id})">Delete</button>
        `;
        taskListElement.appendChild(listItem);
    });
}

function pmv_filterTasks() {
    const filterValue = document.getElementById('pmtsk-filter-input').value.toLowerCase();
    const filteredTasks = pmvtasks.filter(task => 
        task.project_name.toLowerCase().includes(filterValue) ||
        task.user_names.includes(filterValue) ||
        task.start_date.toLowerCase().includes(filterValue) ||
        task.end_date.toLowerCase().includes(filterValue) ||
        (task.status && task.status.toLowerCase().includes(filterValue))
    );
    pmv_displayTasks(filteredTasks);
}

async function pmv_editTask(taskId) {
    const task = pmvtasks.find(t => t.id === taskId);

    // We could add this back later
    // document.getElementById('pmtsk-edit-project').value = task.project_name;
    document.getElementById('pmtsk-edit-user').value = task.user_names;
    document.getElementById('pmtsk-edit-startdate').value = task.start_date;
    document.getElementById('pmtsk-edit-enddate').value = task.end_date;
    // sometimes status is null so this will gives Uncaught (in promise) TypeError: Cannot set properties of null (setting 'value')
    // task.status が null または undefined の場合は空文字列を設定
    document.getElementById('pmtsk-edit-status').value = task.status || '';
    document.getElementById('pmtsk-edit-task-progress').value = task.progress;

    document.getElementById('pmtsk-edit-task-modal').style.display = 'block';

    document.getElementById('pmtsk-edit-task-form').onsubmit = async (e) => {
        e.preventDefault();

        const updatedTask = {
            // project_name: document.getElementById('pmtsk-edit-project').value,
            user_names: document.getElementById('pmtsk-edit-user').value,
            start_date: document.getElementById('pmtsk-edit-startdate').value,
            end_date: document.getElementById('pmtsk-edit-enddate').value,
            status: document.getElementById('pmtsk-edit-status').value,
            progress: document.getElementById('pmtsk-edit-task-progress').value,
        };

        const response = await fetch(`/tasks/${taskId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedTask),
        });

        const response_result = await response.json();
        if (response_result.success) {
            pmv_fetchTasks();
            document.getElementById('pmtsk-edit-task-modal').style.display = 'none';
        } else {
            alert('Failed to update task: ' + response_result.message);
        }
    };

    document.getElementById('pmtsk-cancel-edit').addEventListener('click', () => {
        document.getElementById('pmtsk-edit-task-modal').style.display = 'none';
    });
}

async function pmv_deleteTask(taskId) {
    const confirmation = confirm(`Are you sure you want to delete this task?`);
    if (!confirmation) {
        return;
    }

    try {
        const response = await fetch(`/tasks/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const response_result = await response.json();

        if (response_result.success) {
            pmv_fetchTasks();
        } else {
            alert(`Failed to delete task: ${response_result.detail}`);
        }
    } catch (error) {
        console.error('Error deleting task:', error);
        alert('An error occurred while deleting the task.');
    }
}



