class Filters {
  constructor() {
  }

  main(data_array) {
    new Drop_menu_filters().create_drop_menu(data_array);
    new Input_range_filters().listen_input_range();
    new Chapters_filters().listen_chapters();
  }
}