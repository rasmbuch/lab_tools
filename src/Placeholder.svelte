<script lang="ts">
  interface Props {
    number: string;
    category: string;
    title: string;
  }

  let { number, category, title }: Props = $props();
</script>

<div class="placeholder">
  <div class="placeholder-header">
    <div class="placeholder-header-top">
      <span class="placeholder-number">{number}</span>
      <span class="placeholder-category">{category}</span>
    </div>
    <h1>{title}</h1>
  </div>
  <p class="coming-soon">Coming soon.</p>
</div>

<style>
  .placeholder {
    padding: 60px 64px 80px;
    max-width: 720px;
  }

  .placeholder-header {
    border-bottom: 1px solid var(--color-rule);
    padding-bottom: 26px;
    margin-bottom: 40px;
  }

  .placeholder-header-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 14px;
  }

  .placeholder-number {
    font-family: var(--font-mono);
    font-size: 10.5px;
    color: var(--color-text-faint);
  }

  .placeholder-category {
    font-family: var(--font-ui);
    font-weight: 500;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-text-faint);
  }

  h1 {
    margin: 0;
    font-family: var(--font-ui);
    font-weight: 600;
    font-size: 38px;
    line-height: 1.1;
    letter-spacing: -0.03em;
  }

  .coming-soon {
    font-family: var(--font-mono);
    font-size: 14px;
    color: var(--color-text-faint);
  }
</style>
