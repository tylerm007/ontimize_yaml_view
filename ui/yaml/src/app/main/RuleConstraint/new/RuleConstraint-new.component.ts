import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'RuleConstraint-new',
  templateUrl: './RuleConstraint-new.component.html',
  styleUrls: ['./RuleConstraint-new.component.scss']
})
export class RuleConstraintNewComponent {
  @ViewChild("RuleConstraintForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}