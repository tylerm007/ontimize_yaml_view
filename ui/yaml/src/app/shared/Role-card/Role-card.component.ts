import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Role-card.component.html',
  styleUrls: ['./Role-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Role-card]': 'true'
  }
})

export class RoleCardComponent {


}