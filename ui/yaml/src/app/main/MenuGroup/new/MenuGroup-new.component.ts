import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'MenuGroup-new',
  templateUrl: './MenuGroup-new.component.html',
  styleUrls: ['./MenuGroup-new.component.scss']
})
export class MenuGroupNewComponent {
  @ViewChild("MenuGroupForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'menu_name': "'data'::character varying", 'icon': "'edit_square'::character varying", 'id': "nextval('menu_group_id_seq'::regclass)", 'menu_id': "'data'::character varying"}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}