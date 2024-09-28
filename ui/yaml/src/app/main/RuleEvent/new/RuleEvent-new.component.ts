import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'RuleEvent-new',
  templateUrl: './RuleEvent-new.component.html',
  styleUrls: ['./RuleEvent-new.component.scss']
})
export class RuleEventNewComponent {
  @ViewChild("RuleEventForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}