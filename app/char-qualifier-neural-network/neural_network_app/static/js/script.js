function generate_items_html(items_list) {
    let items_html = ""

    for (let i = 0; i < items_list.length; i++) {
        let item_display = `
        <div class='row-1'>
            <div class='symbol'>${items_list[i]}</div>
            <div class='arsen-progress'>
                <div class="progress-1">
                    <div class="progress-bar-1 char-value" role="progressbar" style="width:0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
            </div>
        </div>`
        items_html += item_display
    }
    return items_html
}
function show_mode() {
    let numbers_html = generate_items_html(number_list)
    numbers_container = document.getElementById("numbers")
    numbers_container.innerHTML = numbers_html

    let alphabet_0_html = generate_items_html(alphabet_0)
    alphabet_0_container = document.getElementById("alphabet-0")
    alphabet_0_container.innerHTML = alphabet_0_html
    
    let alphabet_1_html = generate_items_html(alphabet_1)
    alphabet_1_container = document.getElementById("alphabet-1")
    alphabet_1_container.innerHTML = alphabet_1_html

    let alphabet_2_html = generate_items_html(alphabet_2)
    alphabet_2_container = document.getElementById("alphabet-2")
    alphabet_2_container.innerHTML = alphabet_2_html
}
function generate_buttons_html(items_list) {
    let items_html = ""
    for (let i = 0; i < items_list.length; i++) {
        let item_button = `<button class="button-train" onclick="save_train_image(this)" style="width: 70px;">${items_list[i]}</button>`
        items_html += item_button
    }
    return items_html
}
function train_mode() {
    let numbers_html = generate_buttons_html(number_list)
    numbers_container = document.getElementById("numbers")
    numbers_container.innerHTML = numbers_html

    let alphabet_0_html = generate_buttons_html(alphabet_0)
    alphabet_0_container = document.getElementById("alphabet-0")
    alphabet_0_container.innerHTML = alphabet_0_html

    let alphabet_1_html = generate_buttons_html(alphabet_1)
    alphabet_1_container = document.getElementById("alphabet-1")
    alphabet_1_container.innerHTML = alphabet_1_html

    let alphabet_2_html = generate_buttons_html(alphabet_2)
    alphabet_2_container = document.getElementById("alphabet-2")
    alphabet_2_container.innerHTML = alphabet_2_html
}

function mode_toggle() {
    if (train_mode_status == 0) {
        train_mode()
        train_mode_status = 1
    }
    else {
        show_mode()
        train_mode_status = 0
    }
    
}