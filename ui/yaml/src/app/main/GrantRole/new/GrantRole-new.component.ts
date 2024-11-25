import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'GrantRole-new',
  templateUrl: './GrantRole-new.component.html',
  styleUrls: ['./GrantRole-new.component.scss']
})
export class GrantRoleNewComponent {
  @ViewChild("GrantRoleForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}