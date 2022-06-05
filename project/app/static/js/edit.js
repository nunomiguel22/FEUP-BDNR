

document.getElementById("prop_button").addEventListener("click", () => {

    let prop_key = document.getElementById("prop_key").value;

    let prop_form = document.getElementById("prop_form");

    let label = document.createElement("label", prop_key);
    label.setAttribute("for", prop_key);
    label.innerHTML = prop_key;

    let prop_input = document.createElement("input");
    prop_input.setAttribute("type", "text");
    prop_input.setAttribute("name", prop_key);

    prop_form.appendChild(label);
    prop_form.appendChild(prop_input);
})