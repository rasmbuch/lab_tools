<script lang="ts">
  import { navigate, type Route } from './lib/router';

  interface Props {
    route: Route;
    number: string;
    category: string;
    title: string;
    description: string;
    preview?: string;
  }

  let { route, number, category, title, description, preview = '' }: Props = $props();
</script>

<button class="card" onclick={() => navigate(route)}>
  <div class="card-header">
    <span class="card-number">{number}</span>
    <span class="card-category">{category}</span>
  </div>
  <h2 class="card-title">{title}</h2>
  <p class="card-description">{description}</p>
  {#if preview}
    <div class="card-preview">{preview}</div>
  {/if}
</button>

<style>
  .card {
    display: block;
    text-align: left;
    background: var(--color-surface-card);
    border: 0;
    cursor: pointer;
    padding: 26px 26px 22px;
  }

  .card:hover {
    background: var(--color-surface-card-hover);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }

  .card-number {
    font-family: var(--font-mono);
    font-size: 10.5px;
    color: var(--color-text-faint);
  }

  .card-category {
    font-family: var(--font-ui);
    font-weight: 500;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-text-faint);
  }

  .card-title {
    margin: 14px 0 6px;
    font-family: var(--font-ui);
    font-weight: 600;
    font-size: 25px;
    line-height: 1.12;
    letter-spacing: -0.025em;
    color: var(--color-text);
  }

  .card-description {
    margin: 0 0 20px;
    font-family: var(--font-ui);
    font-size: 12.5px;
    line-height: 1.55;
    color: var(--color-text-muted);
  }

  .card-preview {
    border-top: 1px solid var(--color-rule-light);
    padding-top: 14px;
    font-family: var(--font-mono);
    font-size: 19px;
    line-height: 1.35;
    color: var(--color-text);
  }
</style>
