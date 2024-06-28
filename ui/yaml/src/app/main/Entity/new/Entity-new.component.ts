import { Component, Injector } from '@angular/core';
import { NavigationService } from 'ontimize-web-ngx';

@Component({
  selector: 'Entity-new',
  templateUrl: './Entity-new.component.html',
  styleUrls: ['./Entity-new.component.scss']
})
export class EntityNewComponent {
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}