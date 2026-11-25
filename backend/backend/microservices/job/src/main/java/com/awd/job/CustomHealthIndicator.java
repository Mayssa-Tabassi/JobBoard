
package com.awd.job;

import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.stereotype.Component;

@Component
public class CustomHealthIndicator implements HealthIndicator {

    @Override
    public Health health() {

        boolean serviceAvailable = true;

        if (serviceAvailable) {
            return Health.up()
                    .withDetail("message", "Service Job disponible")
                    .build();
        }

        return Health.down()
                .withDetail("message", "Service Job indisponible")
                .build();
    }
}
