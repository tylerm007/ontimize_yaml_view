import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './ApplicationEntity-card.component.html',
  styleUrls: ['./ApplicationEntity-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.ApplicationEntity-card]': 'true'
  }
})

export class ApplicationEntityCardComponent {


}