import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'MenuItem-new',
  templateUrl: './MenuItem-new.component.html',
  styleUrls: ['./MenuItem-new.component.scss']
})
export class MenuItemNewComponent {
  @ViewChild("MenuItemForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'template_name': "module.jinja", 'icon': "edit_square"}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}