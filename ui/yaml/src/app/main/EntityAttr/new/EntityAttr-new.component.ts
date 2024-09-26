import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'EntityAttr-new',
  templateUrl: './EntityAttr-new.component.html',
  styleUrls: ['./EntityAttr-new.component.scss']
})
export class EntityAttrNewComponent {
  @ViewChild("EntityAttrForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'template_name': "'text'", 'issearch': 'false', 'issort': 'false', 'exclude': 'false', 'visible': 'true', 'isrequired': 'true', 'isenabled': 'true'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}