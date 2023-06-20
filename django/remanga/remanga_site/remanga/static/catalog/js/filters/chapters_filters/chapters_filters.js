class Chapters_filters {
  constructor() {
    this.url_params = ["count_chapters_gte", "count_chapters_lte"];
    this.param_gte = "count_chapters_gte";
    this.param_lte = "count_chapters_lte";
  }

  listen_chapters() {
    const chapters_spans = [...document.querySelectorAll(".Chip_chip__cpsxK")];
    this.first_index_chapters_spans = 0;
    this.last_index_chapters_spans = chapters_spans.length - 1;

    for (const chapter_span of chapters_spans) {
      chapter_span.addEventListener("click", (event) => {
        const values = event.target.innerText.split("-");
        values[0] = values[0].replace(/\D/g, "");
        this.index_clicked_chapter = chapters_spans.indexOf(event.target);

        if (this.index_clicked_chapter == this.first_index_chapters_spans) {
          values.unshift(String());
        } else {
          values.push(String());
        }

        const url_data = new Drop_menu_url_requests().get_url_data(
          this.url_params,
          values,
          false
        );

        this.change_url(url_data);
      });
    }

    this.init_url_chapters_map();
    this.init_url_conditions();
    this.color_chapters(chapters_spans);
  }

  init_url_chapters_map() {
    this.url_chapters_map = new Object();
    for (let search_part of window.location.search.split("&")) {
      for (let url_param of this.url_params) {
        if (search_part.includes(url_param)) {
          this.url_chapters_map[url_param] = search_part.replace(/\D/g, "");
        }
      }
    }
  }

  init_url_conditions() {
    this.empty_url_chapters_values =
      !this.url_chapters_map[this.param_gte] &&
      !this.url_chapters_map[this.param_lte];
  }

  color_chapters(chapters_spans) {
    const storage_indices_clicked_chapters = JSON.parse(
      localStorage.getItem("indices_clicked_chapters")
    );
    const chapter_class_gray = "Chip_gray__uE26d";
    const chapter_class_blue = "Chip_primary__AHVQ0";

    //  remove_storage_empty_array
    if (
      storage_indices_clicked_chapters == null ||
      !window.location.search.includes(this.param_gte) ||
      storage_indices_clicked_chapters.length == 0
    ) {
      localStorage.removeItem("indices_clicked_chapters");
      return;
    }
    //

    for (let index_clicked_chapter of storage_indices_clicked_chapters) {
      chapters_spans[index_clicked_chapter].className = chapters_spans[
        index_clicked_chapter
      ].className.replace(chapter_class_gray, chapter_class_blue);
    }
  }

  change_url(url_data) {
    let new_url_requests_array = url_data[0];
    this.url_repeats_map = url_data[1];

    this.url_change_value(new_url_requests_array);

    let url_replaced = new_url_requests_array.join("");
    if (!url_replaced.includes("?")) {
      url_replaced = url_replaced.replace("&", "?");
    }

    this.save_index_clicked_chapter();
    
    window.location.search = url_replaced;
  }

  url_change_value(new_url_requests_array) {
    if (!window.location.search.includes(this.param_gte)) {
      return;
    }

    // all_chapters_grey
    if (this.replace_empty_url_chapters_values(new_url_requests_array)) {
      return;
    }
    //

    this.all_chapter_values = [
      Object.values(this.url_chapters_map),
      Object.values(this.url_repeats_map),
    ]
      .flatMap((subArr) => subArr)
      .map(Number);

    this.remove_chapters_filters();

    // 0 = ""
    for (let url_param of this.url_params) {
      if (this.url_repeats_map[url_param] == 0) {
        this.url_repeats_map[url_param] = "";
      }
      this.replace_old_url_chapter_request(new_url_requests_array, url_param);
    }
  }

  replace_empty_url_chapters_values(new_url_requests_array) {
    const count_chapters_divs = 4;

    if (this.empty_url_chapters_values) {
      const storage_indices_clicked_chapters = JSON.parse(
        localStorage.getItem("indices_clicked_chapters")
      );

      if (
        storage_indices_clicked_chapters == null ||
        storage_indices_clicked_chapters.length !== count_chapters_divs
      ) {
        for (let url_param of this.url_params) {
          this.replace_old_url_chapter_request(
            new_url_requests_array,
            url_param
          );
        }

        return true;
      }
    }
  }

  remove_chapters_filters() {
    this.filtered_all_chapter_values = this.all_chapter_values;
    let set_all_chapter_values = [...new Set(this.all_chapter_values)];

    if (
      this.filtered_all_chapter_values.length !== set_all_chapter_values.length
    ) {
      this.remove_dublicates_chapter_values();
      this.cleansing_all_chapter_values();
    } else {
      this.clicked_in_one();
    }

    // init_empty_url_chapters_values
    if (this.empty_url_chapters_values) {
      this.filtered_all_chapter_values.unshift(0);
      if (
        this.index_clicked_chapter !== this.first_index_chapters_spans &&
        this.index_clicked_chapter !== this.last_index_chapters_spans
      ) {
        this.filtered_all_chapter_values.pop();
      }
    }
    //

    this.url_repeats_map[this.param_gte] = Math.min(
      ...this.filtered_all_chapter_values
    );
    this.url_repeats_map[this.param_lte] = Math.max(
      ...this.filtered_all_chapter_values
    );
    this.reverse_url_repeats_values();
  }

  remove_dublicates_chapter_values() {
    for (let chapter_value of this.filtered_all_chapter_values) {
      if (
        this.filtered_all_chapter_values.indexOf(chapter_value) !==
        this.filtered_all_chapter_values.lastIndexOf(chapter_value)
      ) {
        this.filtered_all_chapter_values =
          this.filtered_all_chapter_values.filter(
            (item) => item !== chapter_value
          );
      }
    }
  }

  cleansing_all_chapter_values() {
    const index_gte_value = 0;

    if (
      this.filtered_all_chapter_values == false ||
      (this.index_clicked_chapter == this.last_index_chapters_spans &&
        Object.values(this.url_chapters_map).lastIndexOf("") == index_gte_value) // gte not exists lte exists
    ) {
      const no_url_chapters_values = [0, 0];
      this.filtered_all_chapter_values = no_url_chapters_values;
    }
  }

  clicked_in_one() {
    const second_index_chapters_spans = 1;

    if (
      this.index_clicked_chapter == second_index_chapters_spans ||
      this.index_clicked_chapter == this.last_index_chapters_spans
    ) {
      this.filtered_all_chapter_values = this.filtered_all_chapter_values.sort(
        (a, b) => a - b
      );

      const values_array_half = this.all_chapter_values.length / 2;
      const url_chapters_map_values = this.all_chapter_values.slice(
        0,
        values_array_half
      );

      this.filtered_all_chapter_values = url_chapters_map_values;
    }
  }

  reverse_url_repeats_values() {
    const index_lte_value = 1;

    if (
      (Object.values(this.url_chapters_map).indexOf("") == index_lte_value && //gte exists lte not
        this.index_clicked_chapter !== this.last_index_chapters_spans) ||
      (Object.values(this.url_chapters_map).indexOf("") == -1 && //both_chapters_values_exist
        this.index_clicked_chapter == this.last_index_chapters_spans) ||
      (this.empty_url_chapters_values &&
        this.index_clicked_chapter == this.first_index_chapters_spans)
    ) {
      if (
        Object.values(this.url_chapters_map).indexOf("") == index_lte_value &&
        this.index_clicked_chapter == this.first_index_chapters_spans
      ) {
        const no_url_chapters_values = [0, 0];
        this.filtered_all_chapter_values = no_url_chapters_values;
      }

      this.url_repeats_map[this.param_lte] = Math.min(
        ...this.filtered_all_chapter_values
      );
      this.url_repeats_map[this.param_gte] = Math.max(
        ...this.filtered_all_chapter_values
      );
    }
  }

  replace_old_url_chapter_request(new_url_requests_array, url_param) {
    for (let i = 0; i < new_url_requests_array.length; i++) {
      if (new_url_requests_array[i].includes(url_param)) {
        let url_request_name = new_url_requests_array[i].split("=")[0];
        new_url_requests_array[
          i
        ] = `${url_request_name}=${this.url_repeats_map[url_param]}`;
      }
    }
  }

  save_index_clicked_chapter() {
    let storage_indices_clicked_chapters = JSON.parse(
      localStorage.getItem("indices_clicked_chapters")
    );

    this.indices_clicked_chapters = [this.index_clicked_chapter];

    if (storage_indices_clicked_chapters !== null) {
      storage_indices_clicked_chapters =
        storage_indices_clicked_chapters.flatMap((subArr) => subArr); //open subArr

      this.indices_clicked_chapters.push(storage_indices_clicked_chapters);
      this.indices_clicked_chapters = this.indices_clicked_chapters.flatMap(
        (subArr) => subArr
      );

      this.add_color(
        storage_indices_clicked_chapters
      );
    }

    localStorage.setItem(
      "indices_clicked_chapters",
      JSON.stringify(this.indices_clicked_chapters)
    );
  }

  add_color(storage_indices_clicked_chapters) {
    if (
      storage_indices_clicked_chapters.indexOf(this.index_clicked_chapter) == -1 // clicked_index_not_repeated
    ) {
      const all_chapters_indexes = [0, 1, 2, 3];
      this.indices_clicked_chapters = all_chapters_indexes.slice(
        Math.min(...this.indices_clicked_chapters),
        Math.max(...this.indices_clicked_chapters) + 1
      );
    } else {
      this.remove_color();
    }
  }

  remove_color() {
    this.indices_clicked_chapters.shift();

    if (
      this.index_clicked_chapter == this.first_index_chapters_spans ||
      this.index_clicked_chapter == this.last_index_chapters_spans ||
      (!this.indices_clicked_chapters.includes(
        this.first_index_chapters_spans
      ) &&
        !this.indices_clicked_chapters.includes(this.last_index_chapters_spans))
    ) {
      this.indices_clicked_chapters = this.indices_clicked_chapters.filter(
        (item) => item !== this.index_clicked_chapter
      );
    } else {
      this.remove_color_in_one();
    }
  }

  remove_color_in_one() {
    if (
      this.indices_clicked_chapters.indexOf(this.first_index_chapters_spans) ==
      -1
    ) {
      this.indices_clicked_chapters = this.indices_clicked_chapters.slice(
        this.indices_clicked_chapters.indexOf(this.index_clicked_chapter) + 1,
        Math.max(...this.indices_clicked_chapters)
      );
    } else {
      this.indices_clicked_chapters = this.indices_clicked_chapters.slice(
        Math.min(...this.indices_clicked_chapters),
        this.index_clicked_chapter
      );
    }
  }
}
