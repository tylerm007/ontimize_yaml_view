import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Application-card.component.html',
  styleUrls: ['./Application-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Application-card]': 'true'
  }
})

export class ApplicationCardComponent {


}