import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './PageProperty-card.component.html',
  styleUrls: ['./PageProperty-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.PageProperty-card]': 'true'
  }
})

export class PagePropertyCardComponent {


}