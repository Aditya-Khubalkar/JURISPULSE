export interface TimelineEvent {
  id: string;
  caseId: string;
  title: string;
  category: 'hearing' | 'order' | 'filing' | 'evidence';
  date: string;
  description: string;
}
