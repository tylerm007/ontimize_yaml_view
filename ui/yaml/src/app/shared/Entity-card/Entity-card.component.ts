import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Entity-card.component.html',
  styleUrls: ['./Entity-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Entity-card]': 'true'
  }
})

export class EntityCardComponent {


}