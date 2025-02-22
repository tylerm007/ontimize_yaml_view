import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './MenuGroup-card.component.html',
  styleUrls: ['./MenuGroup-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.MenuGroup-card]': 'true'
  }
})

export class MenuGroupCardComponent {


}