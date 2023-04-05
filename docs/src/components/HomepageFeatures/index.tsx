import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Easy to Use',
    Svg: require('@site/static/img/tips_and_updates_FILL0_wght400_GRAD0_opsz48.svg').default,
    description: (
      <>
        All you need is Docker and a certification authority to use to sign certificates!
      </>
    ),
  },
  {
    title: 'Automated',
    Svg: require('@site/static/img/autorenew_FILL0_wght400_GRAD0_opsz48.svg').default,
    description: (
      <>
        Automatically renew certificates in your environment
      </>
    ),
  },
  {
    title: 'OpenSource',
    Svg: require('@site/static/img/frame_source_FILL0_wght400_GRAD0_opsz48.svg').default,
    description: (
      <>
        Investigate the security of ACMEResponder. It is OpenSource forever.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" style={{width: "100px"}} />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
