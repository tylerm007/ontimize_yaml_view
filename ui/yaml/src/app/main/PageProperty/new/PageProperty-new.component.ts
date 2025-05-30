import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'PageProperty-new',
  templateUrl: './PageProperty-new.component.html',
  styleUrls: ['./PageProperty-new.component.scss']
})
export class PagePropertyNewComponent {
  @ViewChild("PagePropertyForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}