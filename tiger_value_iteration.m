function [k,V] = tiger_value_iteration(C,p)
% [k,V] = tiger_value_iteration(C,p)
% Solve for the optimal amount of evidence before acting in the Tiger POMDP
% by value iteration on the smallest necessary set of beliefs.
% Input:
%   C - ratio of cost of being mauled by a tiger to cost of listening once
%   p - probability that tiger is behind the left door if there is a noise
%       from behind the left door (there is always a noise from one door)
% Output:
%   k - weight of evidence (number of times the noise is behind left door
%       over right door) needed for the optimal action to be to open one 
%       door
%   V - value function for different weights of evidence (so long as the
%       prior probability of the tiger being in one room vs the other is
%       symmetric, then so is the environment, and therefore the value
%       function)
%
% David Pfau, 2013

V = [-1/2*C, -(1-p)*C]; % value of opening a door randomly
k = 2;
f  = @(k) (1-p).^k./(p.^k + (1-p).^k); % posterior probability of tiger being behind door we choose after 1 observation
fR = @(k) (p.^(k+1) + (1-p).^(k+1))./(p.^k + (1-p).^k); % predictive probability of hearing a noise behind the door that's more likely to have a tiger
fL = @(k) ((1-p)*p.^k + p*(1-p).^k)./(p.^k + (1-p).^k); % predictive probability of hearing a noise behind the door that's less likely to have a tiger
while 1
    V_ = [V, -C*f(k)];
    V_(2:(k-1)) = max(-C*f(1:(k-2)), -1 + fR(2:(k-1)).*V(3:k) + fL(2:(k-1)).*V(1:(k-2)));
    V_(1) = max(-1/2*C, -1 + V(2));
    if max(abs(V-V_(1:end-1))) < 1e-8, break, end
    V = V_;
    k = k+1;
end
k = find(V<=-C*f(0:length(V)-1),1);
V = V(1:k); % value function is trivial beyond this (just equal to expected cost of being mauled by a tiger)