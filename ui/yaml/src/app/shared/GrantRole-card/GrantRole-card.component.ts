import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './GrantRole-card.component.html',
  styleUrls: ['./GrantRole-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.GrantRole-card]': 'true'
  }
})

export class GrantRoleCardComponent {


}