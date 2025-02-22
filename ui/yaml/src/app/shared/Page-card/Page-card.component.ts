import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Page-card.component.html',
  styleUrls: ['./Page-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Page-card]': 'true'
  }
})

export class PageCardComponent {


}