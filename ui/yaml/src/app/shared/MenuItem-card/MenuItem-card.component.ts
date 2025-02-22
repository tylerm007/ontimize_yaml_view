import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './MenuItem-card.component.html',
  styleUrls: ['./MenuItem-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.MenuItem-card]': 'true'
  }
})

export class MenuItemCardComponent {


}