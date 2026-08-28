<script lang="ts">
  let profileSrc: string | undefined;
  try {
    const mod = import.meta.glob('./assets/images/profile.{jpg,jpeg,png,webp}', { eager: true, import: 'default' });
    const paths = Object.values(mod) as string[];
    profileSrc = paths[0];
  } catch { /* no image yet */ }
</script>

<div class="about">
  <div class="tool-header">
    <div class="tool-header-top">
      <span class="tool-category">personal</span>
    </div>
    <h1>About Me</h1>
  </div>

  <div class="content">
    <div class="profile-section">
      {#if profileSrc}
        <img class="profile-photo" src={profileSrc} alt="Rasmus Buchin" />
      {:else}
        <div class="profile-placeholder">
          <span>Photo</span>
        </div>
      {/if}

      <div class="bio">
        <h2>Rasmus Buchin</h2>
        <p class="role">PhD Student at the University of Hamburg</p>
        <p class="bio-text">
          Hi, I'm Rasmus and this is a small tool I built to use in my daily work.
          I work in XFEL science, primarily interested in it's applications
          in non-linear science and imaging. I have eyed Svelte for quite some time
          but having no background in web dev, never really got around to it.
          This project is mainly that, an excuse to learn Svelte and build something useful for myself.
          If anyone finds some joy or use in this, even better.
        </p>
      </div>
    </div>
  </div>
</div>

<style>
  .about {
    padding: 42px 50px 60px;
    max-width: 800px;
  }

  .tool-header {
    border-bottom: 1px solid var(--color-rule);
    padding-bottom: 26px;
    margin-bottom: 0;
  }

  .tool-header-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 14px;
  }

  .tool-category {
    font-family: var(--font-ui);
    font-weight: 500;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-text-faint);
  }

  h1 {
    margin: 0 0 6px;
    font-family: var(--font-ui);
    font-weight: 600;
    font-size: 38px;
    line-height: 1.1;
    letter-spacing: -0.03em;
  }

  .content {
    border: 1px solid var(--color-rule);
    border-top: 0;
    background: var(--color-surface-card);
    padding: 32px 28px;
  }

  .profile-section {
    display: flex;
    gap: 32px;
    align-items: flex-start;
  }

  .profile-photo {
    width: 180px;
    height: 180px;
    object-fit: cover;
    border-radius: 4px;
    flex: none;
  }

  .profile-placeholder {
    width: 180px;
    height: 180px;
    background: var(--color-surface);
    border: 1px solid var(--color-rule);
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex: none;
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-text-faint);
  }

  .bio {
    flex: 1;
    min-width: 0;
  }

  h2 {
    margin: 0 0 4px;
    font-family: var(--font-ui);
    font-weight: 600;
    font-size: 22px;
    letter-spacing: -0.02em;
  }

  .role {
    margin: 0 0 16px;
    font-family: var(--font-mono);
    font-size: 11.5px;
    color: var(--color-text-faint);
    letter-spacing: 0.01em;
  }

  .bio-text {
    margin: 0;
    font-family: var(--font-ui);
    font-size: 13.5px;
    line-height: 1.7;
    color: var(--color-text-muted);
  }

  @media (max-width: 640px) {
    .profile-section {
      flex-direction: column;
      align-items: center;
      text-align: center;
    }
  }
</style>
