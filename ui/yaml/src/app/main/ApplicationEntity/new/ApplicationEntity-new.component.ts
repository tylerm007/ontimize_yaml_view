import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'ApplicationEntity-new',
  templateUrl: './ApplicationEntity-new.component.html',
  styleUrls: ['./ApplicationEntity-new.component.scss']
})
export class ApplicationEntityNewComponent {
  @ViewChild("ApplicationEntityForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}