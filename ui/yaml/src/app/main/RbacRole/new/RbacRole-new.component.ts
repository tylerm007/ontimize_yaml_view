import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'RbacRole-new',
  templateUrl: './RbacRole-new.component.html',
  styleUrls: ['./RbacRole-new.component.scss']
})
export class RbacRoleNewComponent {
  @ViewChild("RbacRoleForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}