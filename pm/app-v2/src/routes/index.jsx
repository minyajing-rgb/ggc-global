import { createFileRoute } from '@tanstack/react-router';
import PMWorkbench from '@/components/PMWorkbench';

export const Route = createFileRoute('/')({
  ssr: false,
  head: () => ({
    meta: [
      { title: 'Joyce PM · 私人工作台' },
      { name: 'description', content: 'JOYCE PM 私人项目任务工作台：主表、看板、日历、时间线、反馈、阻塞和证据。' },
      { name: 'robots', content: 'noindex, nofollow, noarchive' },
    ],
  }),
  component: PMWorkbench,
});