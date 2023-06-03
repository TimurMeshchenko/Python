class Filter_menu {
  constructor(data, input_number, value_key) {
    this.data = data;
    this.input_number = input_number;
    this.value_key = value_key;
  }
  create_filter_menu() {
    const filter_data = JSON.parse(this.data);
    var div_input = document.querySelectorAll(
      ".jsx-d338f3d1a4c6e9b5.Input_outlined__QwLf6"
    )[this.input_number];

    var div_input_html = div_input.innerHTML;

    const showDropdown = () => {
      div_input.innerHTML += `    
      <div
        tabindex="-1"
        aria-expanded="true"
        role="list"
        class="jsx-f6904a6ed8e0085 jsx-2945355907 select-dropdown"
      >
      `;
      var div_span = document.querySelector(".jsx-f6904a6ed8e0085");
      var div_span_html = div_span.innerHTML;

      filter_data.map((info) => {
        document.querySelector(".jsx-f6904a6ed8e0085").innerHTML += `
          <span
          role="option"
          aria-selected="false"
          aria-label="${info[this.value_key]}"
          tabindex="-1"
          class="jsx-1b57bf17c694e838"
          >${info[this.value_key]}
        </span>
          `;
      });

      this.search(filter_data, div_span_html);

      this.filtration();
    };
    const click_anywhere = (event) => {
      var input = document.querySelectorAll(".jsx-1d2861d85dfb4f6f")[
        this.input_number
      ];

      if (event.target !== input) {
        var all_filter_span = [
          ...document.querySelectorAll(".jsx-1b57bf17c694e838"),
        ];
        if (!all_filter_span.includes(event.target)) {
          div_input.innerHTML = div_input_html;
          return;
        }
      } else if (!document.querySelector(".jsx-f6904a6ed8e0085")) {
        showDropdown();
      }
    };
    document.querySelector("html").addEventListener("click", click_anywhere);

    const save_dropdown = (type_name) => {
      if (window.location.href.includes("?")) {
        if (window.location.href.split("&").pop().includes(type_name)) {
          if (
            this.input_number === Number(localStorage.getItem("input_number"))
          ) {
            showDropdown();
            localStorage.setItem("input_number", "None");
          }
        }        
      }
    };
    save_dropdown("types");
    save_dropdown("genres");
    save_dropdown("categories");
  }

  search(filter_data, div_span_html) {
    var input = document.querySelectorAll(".jsx-1d2861d85dfb4f6f")[
      this.input_number
    ];
    let filteredArr = [];
    var div_span = document.querySelector(".jsx-f6904a6ed8e0085");
    input.addEventListener("keyup", (e) => {
      div_span.innerHTML = div_span_html;
      filteredArr = filter_data.filter((info) =>
        info[this.value_key]
          .toLowerCase()
          .includes(e.target.value.toLowerCase())
      );
      if (filteredArr.length > 0) {
        filteredArr.map((info) => {
          div_span.innerHTML += `
          <span
          role="option"
          aria-selected="false"
          aria-label="${info[this.value_key]}"
          tabindex="-1"
          class="jsx-1b57bf17c694e838"
          >${info[this.value_key]}
        </span>          
          `;
        });
      }
    });
  }

  addQueryParam(name, value) {
    localStorage.setItem("input_number", this.input_number);

    const separator = window.location.href.includes("?") ? "&" : "?";
    window.location.href += `${separator}${name}=${value}`;
  }

  filtration() {
    var all_filter_span = [
      ...document.querySelectorAll(".jsx-1b57bf17c694e838"),
    ];
    all_filter_span.map((span) => {
      span.addEventListener("click", () => {
        var clicked_span = all_filter_span.indexOf(span);
        if (all_filter_span.length < 40) {
          this.addQueryParam("types", clicked_span);
        } else if (all_filter_span.length < 85) {
          this.addQueryParam("genres", clicked_span);
        } else {
          this.addQueryParam("categories", clicked_span);
        }
      });
    });
  }
}
