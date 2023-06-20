class Drop_menu_filters {
  constructor() {}

  create_drop_menu(data_array) {
    this.data_array = data_array;
    this.url_params = ["types", "genres", "categories"];

    this.json_data_parse();
    this.listen_html();

    this.save_default_input_placeholders();
    new Drop_menu_stylization().add_label_input(
      this.url_params,
      this.data_array
    );
    this.restore_drop_menu();
  }

  json_data_parse() {
    for (let i = 0; i < data_array.length; i++) {
      const data = JSON.parse(data_array[i]);
      this.data_array[i] = data;
    }
  }

  listen_html() {
    const click_anywhere = (event) => {
      this.determine_location_click(event);
    };

    document.querySelector("html").addEventListener("click", click_anywhere);
    this.init_delay_vars();
  }

  init_delay_vars() {
    this.timer;
    this.url_request_keys = Array();
    this.url_request_values = Array();
    this.url_repeats = Array();
  }

  save_default_input_placeholders() {
    const divs_label = document.querySelectorAll(".jsx-df39090361a5f2e4");
    this.input_placeholders = Array();
    for (const div_label of divs_label) {
      this.input_placeholders.push(
        div_label.querySelector("input").placeholder
      );
    }
  }

  determine_location_click(event) {
    let parent_clicked_element = event.target;
    const drop_menu_span_class = "jsx-9f9056eddaf3b30b";

    if (parent_clicked_element.tagName == "INPUT") {
      parent_clicked_element = parent_clicked_element.parentNode.parentNode;
    }

    if (parent_clicked_element.className.includes(drop_menu_span_class)) {
      parent_clicked_element =
        parent_clicked_element.parentNode.parentNode.parentNode;
    }

    const parent_div = [...document.querySelectorAll(".jsx-d338f3d1a4c6e9b5")];
    const current_index_clicked_element = parent_div.indexOf(
      parent_clicked_element
    );

    if (
      event.target.className == "Input_input__F9Zao" ||
      event.target.className.includes("Chip_chip__cpsxK")
    ) {
      return;
    }

    this.location_click_drop_menu(event, current_index_clicked_element);
  }

  location_click_drop_menu(event, current_index_clicked_element) {
    if (event.target.innerHTML == "×") {
      this.label_clicked(event, current_index_clicked_element);
      return;
    }

    if (current_index_clicked_element !== -1) {
      this.index_clicked_element = current_index_clicked_element;
      this.init_vars_elements();
      this.check_repeat_click();
      return;
    }

    if (this.drop_menu_element !== undefined) {
      if (this.drop_menu_element.innerHTML.includes(event.target.innerHTML)) {
        this.call_url_requests(event);
        return;
      }

      this.drop_menu_element.remove();
      this.input.value = String();
    }
  }

  label_clicked(event, current_index_clicked_element) {
    const url_data = new Drop_menu_url_requests().delete_label(
      event,
      current_index_clicked_element,
      this.data_array
    );

    this.url_repeats.push(url_data[1]);
    this.url_replaced = url_data[0].join("");
    for (let url_repeat of this.url_repeats) {
      this.url_replaced = this.url_replaced.replace(url_repeat, "");
    }

    this.input_stylization_now(current_index_clicked_element);
    this.change_url(current_index_clicked_element);

    return;
  }

  input_stylization_now(index_clicked_element) {
    if (!this.url_replaced.includes("?")) {
      this.url_replaced = this.url_replaced.replace("&", "?");
    }

    this.restore_input_placeholders();
    new Drop_menu_stylization().add_label_input(
      this.url_params,
      this.data_array,
      this.url_replaced.replace("?", "")
    );
    new Drop_menu_stylization().color_clicked_span(
      this.url_params[index_clicked_element],
      this.url_replaced.replace("?", "")
    );
  }

  change_url(current_index_clicked_element) {
    if (this.timer !== undefined) {
      clearTimeout(this.timer);
    }
    this.timer = setTimeout(() => {
      this.before_window_reload(current_index_clicked_element);
      window.location.search = this.url_replaced;
    }, 700);
  }

  before_window_reload(index_clicked_element) {
    const drop_menu_element = document.querySelector(".jsx-f6904a6ed8e0085");
    if (drop_menu_element) {
      localStorage.setItem("index_clicked_element", index_clicked_element);
      localStorage.setItem("drop_menu_scroll", drop_menu_element.scrollTop);
    }
  }

  init_vars_elements() {
    this.div_input = document.querySelectorAll(".jsx-d338f3d1a4c6e9b5")[
      this.index_clicked_element
    ];
    this.drop_menu_element = document.querySelector(".jsx-f6904a6ed8e0085");
    this.input = document.querySelectorAll(".jsx-1d2861d85dfb4f6f")[
      this.index_clicked_element
    ];
  }

  check_repeat_click() {
    const drop_menu_class = ".jsx-f6904a6ed8e0085";
    if (!this.div_input.querySelector(drop_menu_class)) {
      this.show_drop_menu();
    }
  }

  show_drop_menu() {
    const inputs = document.querySelectorAll(".jsx-1d2861d85dfb4f6f");
    for (let input of inputs) {
      input.value = String();
    }

    if (this.drop_menu_element) {
      this.drop_menu_element.remove();
    }

    this.div_input.innerHTML += `
      <div
        tabindex="-1"
        aria-expanded="true"
        role="list"
        class="jsx-f6904a6ed8e0085 jsx-2945355907 select-dropdown"
      >
      `;

    this.init_vars_elements();

    const empty_drop_menu = this.drop_menu_element.innerHTML;

    const data = this.data_array[this.index_clicked_element];
    let value_key = Object.keys(data[0]);
    value_key = value_key[value_key.length - 1];

    data.map((info) => {
      this.drop_menu_content(info[value_key]);
    });

    this.call_after_show_drop_menu(empty_drop_menu, data, value_key);
  }

  drop_menu_content(value) {
    this.drop_menu_element.innerHTML += `
        <span
        role="option"
        aria-selected="false"
        aria-label="${value}"
        tabindex="-1"
        class="jsx-1b57bf17c694e838"
        >${value}
      </span>
        `;
  }

  call_after_show_drop_menu(empty_drop_menu, data, value_key) {
    this.input.focus();

    new Drop_menu_stylization().color_clicked_span(
      this.url_params[this.index_clicked_element]
    );
    this.search(empty_drop_menu, data, value_key);
    new Drop_menu_stylization().change_drop_menu_height(
      Number(this.index_clicked_element)
    );
  }

  search(empty_drop_menu, data, value_key) {
    let filteredArr = [];
    const item_selected = document.querySelectorAll(".item-selected");

    this.input.addEventListener("keyup", (event) => {
      this.drop_menu_element.innerHTML = empty_drop_menu;
      filteredArr = data.filter((info) =>
        info[value_key].toLowerCase().includes(event.target.value.toLowerCase())
      );
      if (filteredArr.length) {
        filteredArr.map((info) => {
          this.drop_menu_content(info[value_key]);
        });
      }
      new Drop_menu_stylization().search_color_span(item_selected);
    });
  }

  call_url_requests(event) {
    const all_drop_menu_spans = [
      ...document.querySelectorAll(".jsx-1b57bf17c694e838"),
    ];
    const index_clicked_span = all_drop_menu_spans.indexOf(event.target);
    this.url_request_keys.push(this.url_params[this.index_clicked_element]);
    this.url_request_values.push(index_clicked_span);

    this.drop_menu_stylization_now();
  }

  drop_menu_stylization_now() {
    const url_data = new Drop_menu_url_requests().get_url_data(
      this.url_request_keys,
      this.url_request_values
    );

    this.url_replaced = url_data[0].join("");
    for (let url_repeat of url_data[1]) {
      this.url_replaced = this.url_replaced.replace(url_repeat, "");
    }

    this.input_stylization_now(this.index_clicked_element);
    this.change_url(this.index_clicked_element);
  }

  restore_input_placeholders() {
    const divs_label = document.querySelectorAll(".jsx-df39090361a5f2e4");
    for (let i = 0; i < divs_label.length; i++) {
      divs_label[i].querySelector("input").placeholder =
        this.input_placeholders[i];
    }
  }

  restore_drop_menu() {
    if (localStorage.getItem("index_clicked_element") != null) {
      // СПОСОБ различать блок фильтрации исключений от обычного

      // let div_inputs = document.querySelectorAll(".jsx-d338f3d1a4c6e9b5");
      // let parent_divs_active = document.activeElement.parentNode.parentNode.parentNode.parentNode;
      // let filter_title_class = "flex"

      // if(parent_divs_active.previousElementSibling.className.includes(
      //     filter_title_class
      //   )) {
      //     let count_div_first_block = 3
      //     for (
      //       let index_div_input = 0;
      //       index_div_input < count_div_first_block;
      //       index_div_input++
      //     ) {
      //       if(
      //         div_inputs[index_div_input].innerHTML.includes(
      //           document.activeElement.outerHTML
      //         )
      //       ) {
      //     };
      //   }
      // }
      this.index_clicked_element = localStorage.getItem(
        "index_clicked_element"
      );

      this.init_vars_elements();

      this.show_drop_menu();

      this.drop_menu_element.scrollTo(
        0,
        Number(localStorage.getItem("drop_menu_scroll"))
      );
      localStorage.removeItem("index_clicked_element");
      localStorage.removeItem("drop_menu_scroll");
    }
  }
}